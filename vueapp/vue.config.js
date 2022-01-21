// vue.config.js

const Dotenv = require('dotenv-webpack');
/**
 * @type {import('@vue/cli-service').ProjectOptions}
 */

module.exports = {
  configureWebpack: {
    plugins: [
      new Dotenv()
    ]
  }
}