import mongoose from 'mongoose';

const drugSchema = mongoose.Schema({
  drugname: { type: String, unique: true }
});

const Drug = mongoose.model('Drug', drugSchema);
module.exports = Drug;

