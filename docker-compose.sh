path=`eval echo "$1"`
folder=$(dirname "$path")    
DIR=$(cd "$folder"; pwd)/$(basename "$path"); 
echo DIR=$DIR

{
    cp -R app rasa_core
    cp -R app rasa_nlu
    cp -R app/models/nlu rasa_nlu/app/models
} 

wait
# docker-compose down && docker-compose rm -f && docker-compose build --no-cache && docker-compose up