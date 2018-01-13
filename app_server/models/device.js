import mongoose from 'mongoose';

const deviceSchema = mongoose.Schema({
  deviceId: { type: String, unique: true },
  password: String,
  connected: Boolean
});

const Device = mongoose.model('Device', deviceSchema);
module.exports = Device;

