import axios from 'axios';

const dataSources = {
  PoultryTransBoiledChickenData: {
    '白肉雞(2.0Kg以上)': '白肉雞（2.0kg以上）',
    '白肉雞(1.75-1.95Kg)': '白肉雞（1.75~1.95kg）',
    '白肉雞(門市價高屏)': '白肉雞（門市價，高屏）',
    '雞蛋(產地)': '雞蛋（產地）',
  },
  PoultryTransLocalChickenData: {
    黑羽土雞公舍飼: '黑羽土雞（南區，公，舍飼）',
    黑羽土雞母舍飼: '黑羽土雞（南區，母，舍飼）',
  },
  PoultryTransGooseDuckData: {
    '肉鵝(白羅曼)': '肉鵝（白羅曼）',
    '正番鴨(公)': '正番鴨（公）',
    '土番鴨(75天)': '土番鴨（75天）',
    '鴨蛋(新蛋)(台南)': '鴨蛋（新蛋，台南）',
  },
  PoultryTransLocalRedChickenData: {
    紅羽土雞北區: '紅羽土雞（北區）',
    紅羽土雞中區: '紅羽土雞（中區）',
    紅羽土雞南區: '紅羽土雞（南區）',
  },
  PoultryTransLocalBlackChickenData: {
    '黑羽土雞舍飼(南區)公': '黑羽土雞（南區，公，舍飼）',
    '黑羽土雞舍飼(南區)母': '黑羽土雞（南區，母，舍飼）',
  },
};

function getDataUrl(src) {
  const url = 'https://cors-anywhere.herokuapp.com/';
  return url + `https://data.coa.gov.tw/Service/OpenData/FromM/${src}.aspx`;
}

function processRawData(rawData, fields) {
  const result = {};
  for (const node of rawData) {
    const date = node['日期'];
    for (const [field, name] of Object.entries(fields)) {
      if (!Object.prototype.hasOwnProperty.call(result, name))
        result[name] = [];
      let rawValue = node[field];
      if (rawValue != '休市' && rawValue != '-') {
        if (rawValue.includes('..')) rawValue = rawValue.replace('..', '.');
        if (rawValue.includes('-')) {
          const rawValues = rawValue.split('-');
          rawValue = (Number(rawValues[0]) + Number(rawValues[1])) / 2;
        }
        const value = Number(rawValue);
        if (value > 0) result[name].push({ date: date, value: value });
      }
    }
  }
  return result;
}

let data = {};

export function getData() {
  return Promise.all(
    Object.entries(dataSources).map(async ([src, fields]) => {
      const response = await axios.get(getDataUrl(src));
      return processRawData(response.data, fields);
    })
  ).then((results) => {
    results.forEach((result) => (data = Object.assign(data, result)));
    localStorage.setItem('data', JSON.stringify(data));
  });
}

export const dataUnit = '元／台斤';

export const dataItems = [
  { icon: '🐔', title: '白肉雞（2.0kg以上）', link: '/01' },
  { icon: '🐔', title: '白肉雞（1.75~1.95kg）', link: '/02' },
  { icon: '🐔', title: '白肉雞（門市價，高屏）', link: '/03' },
  { icon: '🥚', title: '雞蛋（產地）', link: '/04' },
  { icon: '🦢', title: '肉鵝（白羅曼）', link: '/05' },
  { icon: '🦆', title: '正番鴨（公）', link: '/06' },
  { icon: '🦆', title: '土番鴨（75天）', link: '/07' },
  { icon: '🥚', title: '鴨蛋（新蛋，台南）', link: '/08' },
  { icon: '🐓', title: '紅羽土雞（北區）', link: '/09' },
  { icon: '🐓', title: '紅羽土雞（中區）', link: '/10' },
  { icon: '🐓', title: '紅羽土雞（南區）', link: '/11' },
  { icon: '🐓', title: '黑羽土雞（南區，公，舍飼）', link: '/12' },
  { icon: '🐓', title: '黑羽土雞（南區，母，舍飼）', link: '/13' },
];

export default data;
