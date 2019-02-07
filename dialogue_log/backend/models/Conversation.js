import mongoose from 'mongoose';
const Schema = mongoose.Schema;
let Conversation = new Schema({
    sender_id: {
        type: String
    }
});

export default mongoose.model('Conversation', Conversation);