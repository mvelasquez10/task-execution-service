
import http from 'k6/http';
import { check, sleep } from 'k6';
import { options } from './config.js';
import { uuidv4 } from 'https://jslib.k6.io/k6-utils/1.4.0/index.js';

export { options };

export default function () {
  const configuration_id = uuidv4();
  const location_id = 'my-location';
  const now = new Date().toISOString();

  const headers = {
    'Content-Type': 'application/json',
  };

  // Create Task
  const createTaskResponse = http.post(
    'http://app:8000/tasks/',
    JSON.stringify({
      configuration_id: configuration_id,
      location_id: location_id,
      due_date: now,
    }),
    { headers: headers }
  );

  check(createTaskResponse, {
    'CreateTask is successful': (r) => r.status == 200,
  });

  const task_id = JSON.parse(createTaskResponse.body).id;

  // Get Task
  const getTaskResponse = http.get(`http://app:8000/tasks/${task_id}`);
  check(getTaskResponse, {
    'GetTask is successful': (r) => r.status == 200,
  });

  // Complete Task
  const completeTaskResponse = http.put(`http://app:8000/tasks/${task_id}/complete`);
  check(completeTaskResponse, {
    'CompleteTask is successful': (r) => r.status == 200,
  });

  // Delete Task
  const deleteTaskResponse = http.del(`http://app:8000/tasks/${task_id}`);
  check(deleteTaskResponse, {
    'DeleteTask is successful': (r) => r.status == 204,
  });

  // Get All Tasks
  const getAllTasksResponse = http.get('http://app:8000/tasks');
  check(getAllTasksResponse, {
    'GetAllTasks is successful': (r) => r.status == 200,
  });

  sleep(1);
}
