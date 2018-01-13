import mongoose from 'mongoose';

const messageSchema = mongoose.Schema({
  me: String,
  you: String,
  content: String,
  time: Number
});

const Message = mongoose.model('Message', messageSchema);
module.exports = Message;