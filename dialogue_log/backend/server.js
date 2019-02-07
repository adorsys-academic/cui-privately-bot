import express from 'express';
import cors from 'cors';
import bodyParser from 'body-parser';
import mongoose from 'mongoose';
import Conversation from './models/Conversation'

const app = express();
const router = express.Router();
app.use(cors({
    // credentials: true,
    // origin: true
}));

app.use(bodyParser.json());
mongoose.connect('mongodb://<MONGO_URL>', {
    useNewUrlParser: true
});
const connection = mongoose.connection;
connection.once('open', () => {
    console.log('MongoDB database connection established successfully!');
});

router.route('/conversations').get((req, res) => {
    Conversation.find((err, conversations) => {
        if (err)
            console.log(err);
        else
            res.json(conversations);
    });
});

router.route('/test').get((req, res) => {
    res.send('Hello World!')

});

router.route('/conversations/delete/:id').get((req, res) => {
    Conversation.findByIdAndRemove({
        _id: req.params.id
    }, (err, conversation) => {
        if (err)
            res.json(err);
        else
            res.json('Removed successfully');
    });
});

app.use('/', router);
app.listen(4221, () => console.log(`Express server running on port 4221`));