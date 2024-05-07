const kue = require('kue');

const createPushNotificationsJobs = (jobs, queue) => {
  if (!Array.isArray(jobs)) {
    throw new Error('Jobs is not an array');
  }

  jobs.forEach((jobData) => {
    const job = queue
      .create('push_notification_code_3', jobData)
      .save((err) => {
        if (err) {
          return;
        }
        console.log(`Notification job created: ${job.id}`);
      });

    // listen for job completion
    job.on('complete', () => {
      console.log(`Notification job ${job.id} completed`);
    });

    // listen for job failure
    job.on('failed', (err) => {
      console.log(`Notification job ${job.id} failed: ${err}`);
    });

    // listen for job progress
    job.on('progress', (progress) => {
      console.log(`Notification job ${job.id} ${progress}% complete`);
    });
  });
};


module.exports = createPushNotificationsJobs;
