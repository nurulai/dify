module.exports = {
    apps : [
        {
            name: "dify-web",
            script: "yarn",
            args: "start",
            exec_mode: "fork",
            interpreter: "node@18.20.5",
            env: {
                NODE_OPTIONS: "-r dotenv/config",
                YARN_PORT: 18004
            },
            watch: false,
        }
    ]
};