const chai = require('chai');
const kue = require('kue');
const createPushNotificationsJobs = require('./8-job');

const { expect } = chai;

describe('createPushNotificationsJobs', () => {
  let queue;

  beforeEach(() => {
    // create a Kue queue in test mode
    queue = kue.createQueue();
    queue.testMode.enter();
  });

  afterEach(() => {
    // clear the queue and exit test mode after each test
    queue.testMode.clear();
    queue.testMode.exit();
  });

  it('should display an error message if jobs is not an array', () => {
    expect(() => createPushNotificationsJobs('invalid', queue)).throw(
      'Jobs is not an array'
    );
  });

  it('should create two new jobs to the queue', () => {
    const jobs = [
      { phoneNumber: '4153518780', message: 'Test message 1' },
      { phoneNumber: '4153518781', message: 'Test message 2' },
    ];

    createPushNotificationsJobs(jobs, queue);

    // check if jobs were added to the queue
    //expect(queue.testMode.jobs.length).toBe(2);
    setTimeout(() => {
      expect(queue.testMode.jobs.length).to.equal(2);
      done();
    }, 100);
  }).timeout(5000);
});
