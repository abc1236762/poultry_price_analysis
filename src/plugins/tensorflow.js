import * as tf from '@tensorflow/tfjs';

if (typeof global !== 'undefined' && global.toString() === '[object global]') {
  require('@tensorflow/tfjs-node');
} else {
  require('@tensorflow/tfjs-backend-webgl');
}

export default tf;
