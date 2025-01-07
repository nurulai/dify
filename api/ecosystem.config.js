module.exports = {
    apps: [
        {
            name: 'dify-api',
            script: './start-api.sh',
            wait_ready: true,
            autorestart: true,
            max_restarts: 5,
            instances: "1"
        },
        {
            name: 'dify-worker',
            script: './start-worker.sh',
            wait_ready: true,
            autorestart: true,
            max_restarts: 5,
            instances: "1"
        },
    ]
}