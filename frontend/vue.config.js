module.exports = {
  outputDir: '../dist',
  transpileDependencies: ['vuetify'],
  configureWebpack: {
    devtool: 'source-map',
  },
  chainWebpack: (config) => {
    config.plugin('html').tap((args) => {
      args[0].title = '家禽價格分析';
      return args;
    });
  },
  pluginOptions: {
    electronBuilder: {
      outputDir: '../dist_electron',
      nodeIntegration: true,
      builderOptions: {
        appId: 'xyz.yurina.poultrypriceanalysis',
        productName: '家禽價格分析',
      },
    },
  },
};
