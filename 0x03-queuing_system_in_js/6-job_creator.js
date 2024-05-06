const kue = require('kue');
const queue = kue.createQueue();

const jobData = {
  phoneNumber: '0123456789',
  message: 'Hello World, this is a message for the job',
};

// Create a job in the queue
const job = queue.create('push_notification_code', jobData).save((err) => {
  if (err) {
    // failed to create job
    return;
  }
  console.log('Notification job created', job.id);
});

// job completion listener event
job.on('complete', () => {
  console.log('Notification job completed');
});

job.on('failed', () => {
  console.log('Notification job failed');
});
