const kue = require('kue');
const queue = kue.createQueue({
  jobEvents: false,
  concurrency: 2, //process two jobs at a time
});

const blacklistedNumbers = ['4153518780', '4153518781'];

const sendNotification = (phoneNumber, messsage, job, done) => {
  job.progress(0, 100);

  if (blacklistedNumbers.includes(phoneNumber)) {
    const error = new Error(`Phone number ${phoneNumber} is blacklisted`);
    done(error);
  } else {
    job.progress(50, 100); // Track progress to 50%
    console.log(
      `Sending notification to ${phoneNumber}, with message: ${messsage}`
    );
    done();
  }
};

// process jobs in the queue
queue.process('push_notification_code_2', 2, (job, done) => {
  const { phoneNumber, message } = job.data;
  sendNotification(phoneNumber, message, job, done);
});
