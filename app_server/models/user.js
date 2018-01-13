import mongoose from 'mongoose';
import Device from './device';

const userSchema = mongoose.Schema({
  username: { type: String, unique: true },
  password: String,
  connected: Boolean,
  prescription: [{
    drug: String,
    time: Date,
    amount: Number
  }],
  device: {
        type: mongoose.Schema.ObjectId,
        ref: 'Device'
  }
});

const User = mongoose.model('User', userSchema);
module.exports = User;

