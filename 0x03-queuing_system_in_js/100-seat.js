const express = require('express');
const redis = require('redis');
const { promisify } = require('util');
const kue = require('kue');

const app = express();
const port = 1245;

// Redis client
const client = redis.createClient();

// Promisify redis methods
const getAsync = promisify(client.get).bind(client);
const setAsync = promisify(client.set).bind(client);

// initialize available seats and reservation status
let numberOfAvailableSeats = 50;
let reservationEnabled = true;

const reserveSeat = async (number) => {
  // reserve a seat in redis
  await setAsync('available_seats', number);
};

const getCurrentAvailableSeats = async () => {
  // get current available seats from redis
  const availableSeats = await getAsync('available_seats');
  return availableSeats ? parseInt(availableSeats) : 0;
};

const queue = kue.createQueue();

app.use(express.json());

app.get('/available_seats', (req, res) => {
  res.json({ numberOfAvailableSeats });
});

app.get('/reserve_seat', (req, res) => {
  if (!reservationEnabled) {
    res.json({ status: 'Reservation are blocked' });
  } else {
    queue.create('reserve_seat').save();
    res.json({ status: 'Reservation in process' });
  }
});

app.get('/process', async (req, res) => {
  res.json({ status: 'Queue processing ' });

  queue.process('reserve_seat', async (job, done) => {
    const currentAvailableSeats = await getCurrentAvailableSeats();
    if (currentAvailableSeats === 0) {
      reservationEnabled = false;
      done(new Error('Not enough seats available'));
    } else {
      numberOfAvailableSeats--;
      await reserveSeat(numberOfAvailableSeats);
      if (numberOfAvailableSeats === 0) {
        reservationEnabled = false;
      }
      console.log(`Seat reservation job ${job.id} completed`);
      done();
    }
  });
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
