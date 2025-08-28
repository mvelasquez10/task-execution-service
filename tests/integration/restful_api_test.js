
const axios = require('axios');
const { expect } = require('chai');
const { v4: uuidv4 } = require('uuid');

const API_URL = 'http://localhost:8000';

describe('RESTful API Integration Tests', () => {
    let taskId;
    const configurationId = uuidv4();
    const locationId = 'test-location';
    const userId = 'test-user';
    const roleId = 'test-role';
    const dueDate = new Date(new Date().getTime() + 3600 * 1000); // 1 hour from now

    it('should create a new task', async () => {
        const response = await axios.post(`${API_URL}/tasks`, {
            configuration_id: configurationId,
            location_id: locationId,
            user_id: userId,
            role_id: roleId,
            due_date: dueDate.toISOString(),
        });
        expect(response.status).to.equal(201);
        expect(response.data).to.have.property('id');
        taskId = response.data.id;
    });

    it('should get a task by id', async () => {
        const response = await axios.get(`${API_URL}/tasks/${taskId}`);
        expect(response.status).to.equal(200);
        expect(response.data).to.have.property('id', taskId);
    });

    it('should get all tasks', async () => {
        const response = await axios.get(`${API_URL}/tasks`);
        expect(response.status).to.equal(200);
        expect(response.data).to.be.an('array');
    });

    it('should complete a task', async () => {
        const response = await axios.put(`${API_URL}/tasks/${taskId}/complete`);
        expect(response.status).to.equal(200);
        expect(response.data).to.have.property('status', 'completed');
    });

    it('should delete a task', async () => {
        const response = await axios.delete(`${API_URL}/tasks/${taskId}`);
        expect(response.status).to.equal(204);
    });

    it('should return a healthy status', async () => {
        const response = await axios.get(`${API_URL}/health`);
        expect(response.status).to.equal(200);
        expect(response.data).to.have.property('status', 'healthy');
        expect(response.data.dependencies).to.deep.equal({
            repository: 'CLOSED',
            event_sender: 'CLOSED',
        });
    });
});
