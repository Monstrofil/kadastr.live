// vue.config.js

const Dotenv = require('dotenv-webpack');
const webpack = require('webpack');
const fs = require('fs');
const packageJson = fs.readFileSync('./package.json');
const version = JSON.parse(packageJson).version || 0;
/**
 * @type {import('@vue/cli-service').ProjectOptions}
 */

module.exports = {
  configureWebpack: {
    plugins: [
        new Dotenv(),
        new webpack.DefinePlugin({
                'process.build': {
                    version: '"' + version + '"'
                }
            })
    ]
  }
}