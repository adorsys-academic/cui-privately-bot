from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import io

import mock
import responses
from rasa_nlu.project import Project, load_from_server
from rasa_nlu.utils import EndpointConfig


def test_dynamic_load_model_with_exists_model():
    MODEL_NAME = 'model_name'

    def mocked_init(*args, **kwargs):
        return None

    with mock.patch.object(Project, "__init__", mocked_init):
        project = Project()

        project._models = (MODEL_NAME, )

        project.pull_models = None

        result = project._dynamic_load_model(MODEL_NAME)

        assert result == MODEL_NAME


def test_dynamic_load_model_with_refresh_exists_model():
    MODEL_NAME = 'model_name'

    def mocked_init(*args, **kwargs):
        return None

    def mocked_search_for_models(self):
        self._models = (MODEL_NAME, )

    with mock.patch.object(Project, "__init__", mocked_init):
        with mock.patch.object(Project, '_search_for_models', mocked_search_for_models):
            project = Project()

            project._models = ()

            project.pull_models = None

            result = project._dynamic_load_model(MODEL_NAME)

            assert result == MODEL_NAME


def test_dynamic_load_model_with_refresh_not_exists_model():
    LATEST_MODEL_NAME = 'latest_model_name'

    def mocked_init(*args, **kwargs):
        return None

    def mocked_search_for_models(self):
        pass

    def mocked_latest_project_model(self):
        return LATEST_MODEL_NAME

    with mock.patch.object(Project, "__init__", mocked_init):
        with mock.patch.object(Project, "_search_for_models", mocked_search_for_models):
            with mock.patch.object(Project, "_latest_project_model", mocked_latest_project_model):
                project = Project()

                project._models = ()

                project.pull_models = None

                result = project._dynamic_load_model('model_name')

                assert result == LATEST_MODEL_NAME


def test_dynamic_load_model_with_model_is_none():
    LATEST_MODEL_NAME = 'latest_model_name'

    def mocked_init(*args, **kwargs):
        return None

    def mocked_search_for_models(self):
        pass

    def mocked_latest_project_model(self):
        return LATEST_MODEL_NAME

    with mock.patch.object(Project, "__init__", mocked_init):
        with mock.patch.object(Project, "_search_for_models", mocked_search_for_models):
            with mock.patch.object(Project, "_latest_project_model", mocked_latest_project_model):
                project = Project()

                project._models = ()

                project.pull_models = None

                result = project._dynamic_load_model(None)

                assert result == LATEST_MODEL_NAME


@responses.activate
def test_project_with_model_server(zipped_nlu_model):
    fingerprint = 'somehash'
    model_endpoint = EndpointConfig('http://server.com/models/nlu/tags/latest')

    # mock a response that returns a zipped model
    with io.open(zipped_nlu_model, 'rb') as f:
        responses.add(responses.GET,
                      model_endpoint.url,
                      headers={"ETag": fingerprint,
                               "filename": "my_model_xyz.zip"},
                      body=f.read(),
                      content_type='application/zip',
                      stream=True)
    project = load_from_server(model_server=model_endpoint)
    assert project.fingerprint == fingerprint
