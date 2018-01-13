import { Router } from 'express';
import { Device, User, Message, Drug } from './models';

const router = new Router();

// Write your restful api here:
const returnRouter = (io) => {
  router.get('/devices', (req, res) => {
    Device.find().exec((err, devices) => {
      console.log(devices);
      res.json(devices);
    });
  });

  router.get('/drugs', (req, res) => {
    Drug.find().exec((err, drugs) => {
      res.json(drugs);
    });
  });

  router.post('/auth/login', (req, res) => {
    const { username, password } = req.body;
    User.findOne({
      username: username
    }, (err, user) => {
      if (err) {
          throw err;
      } else if (!user){
        console.log('username not found; create new account');
        User.create({
          username: username,
          password: password,
          connected: true,
          drugs:[],
          device: null
        }, (err, user) => {
          if (err) {
            throw err;
          }
          res.json({'success': true});
        });
      } else {
        if (user.password !== password) {
          console.log('wrong password');
          res.json({'success': false});
        } else {
          res.json({'success': true});        
        }
      }
    }); 
  });

  router.post('/auth/logout', (req, res) => {
    const { username } = req.body;
    User.findOneAndUpdate({
      username: username
    }, {
      connected: false
    }, (err, user) => {
      if (err) {
        throw err;
      } else if (!user){
      } else {
          res.json(user);
      }
    }); 
  });

  router.get('/message/:user1/:user2', (req, res) => {
    let me = req.params.user1;
    let you = req.params.user2;
    
    Message.find({
      $or: [ { me: me, you: you}, {me: you, you: me} ]
    }, (err, messages) => {
      if (err) {
        throw err;
      } else {
        res.json(messages);
      }
    }); 
  });

  router.get('/user/:name', (req, res) => {
    User.findOne({
      username: req.params.name
    }, (err, user) => {
      if(err) throw err;
      else {
        console.log(`req.params: ${req.params.name}`);
        console.log(`user: ${user}`);
        res.json(user);
      }
    });
  });

  router.use((req, res) => {
    res.send('404');
  });

  io.sockets.on('connection', socket => {
    console.log("someone is connected");

    socket.on('message', message => {
      Message.create({
        me: message.me,
        you: message.you,
        content: message.content,
        time: message.time
      }, (err, message) => {
        if (err) {
          throw err;
        } else {
        }
      });
      io.sockets.emit('message', message);
    });

    socket.on('putUser', user => {
      console.log(`user: ${user.username}`);
      user.prescription = user.prescription.map(inst => {
        inst.time = new Date(inst.time);
        return inst;
      });
      User.findOneAndUpdate({
        username: user.username
      }, user, (err, message) => {
        if (err) {
          throw err;
        } else {
          console.log(message);
        }
      });
    });

    socket.on('register', (info) => {
      io.sockets.emit('register', info);
    });
    socket.on('unregister', (username) => {
      console.log("unregister");
      io.sockets.emit('unregister', username);
    });
    socket.on('disconnect', () => {
      console.log("disconnect from server");
    });
  });

  return router;
}

module.exports = returnRouter;
