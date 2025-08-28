
const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');
const { expect } = require('chai');
const { v4: uuidv4 } = require('uuid');

const PROTO_PATH = __dirname + '/../../src/infrastructure/task.proto';
const packageDefinition = protoLoader.loadSync(PROTO_PATH, {
    keepCase: true,
    longs: String,
    enums: String,
    defaults: true,
    oneofs: true
});
const taskProto = grpc.loadPackageDefinition(packageDefinition).task;
const client = new taskProto.TaskService('localhost:50051', grpc.credentials.createInsecure());

describe('gRPC API Integration Tests', () => {
    let taskId;
    const configurationId = uuidv4();
    const locationId = 'test-location';
    const userId = 'test-user';
    const roleId = 'test-role';
    const dueDate = Math.floor(new Date().getTime() / 1000) + 3600; // 1 hour from now

    it('should create a new task', (done) => {
        client.createTask({
            configuration_id: configurationId,
            location_id: locationId,
            user_id: userId,
            role_id: roleId,
            due_date: dueDate
        }, (err, response) => {
            expect(err).to.be.null;
            expect(response).to.have.property('id');
            taskId = response.id;
            done();
        });
    });

    it('should get a task by id', (done) => {
        client.getTask({ task_id: taskId }, (err, response) => {
            expect(err).to.be.null;
            expect(response).to.have.property('id', taskId);
            done();
        });
    });

    it('should get all tasks', (done) => {
        client.getAllTasks({ page: 1, limit: 10 }, (err, response) => {
            expect(err).to.be.null;
            expect(response.tasks).to.be.an('array');
            done();
        });
    });

    it('should complete a task', (done) => {
        client.completeTask({ task_id: taskId }, (err, response) => {
            expect(err).to.be.null;
            expect(response).to.have.property('completed', true);
            done();
        });
    });

    it('should delete a task', (done) => {
        client.deleteTask({ task_id: taskId }, (err, response) => {
            expect(err).to.be.null;
            done();
        });
    });
});
