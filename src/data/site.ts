// Personal information is optional. Empty contact fields will be hidden.
export const profile = {
  name: 'shaw chenyu',
  initials: 'sc',
  university: '上海大学',
  major: '电子信息',
  enrollmentYear: '',
  stage: '研究生',
  interests: ['VR图像质量评价', 'AIGC与UGC混合图片数据库和算法'],
  bio: '在学习中提问，在实践中理解。记录计算机视觉的学习过程，也记录研究生活里的思考。',
  email: '2942219735@qq.com',
  github: '',
  avatar: '/images/avatar.jpg',
};

export const site = {
  title: 'shaw 的手记',
  englishTitle: 'NOTES & LITTLE THOUGHTS',
  description: '记录AIGC与UGC混合VR图片数据库和质量评价算法的学习、实验与研途思考。',
  heroTitle: '把学习的点滴，\n写为成长的轨迹。',
  heroDescription: '从一个概念、一篇论文、一次实验开始。把学习的来路写下来，让思考有迹可循。',
};

export const categories = ['基础学习', '论文阅读', '实验与复现', '研途随笔'] as const;
export const navigation = [
  { label: '首页', path: '/' },
  { label: '文章', path: '/blog/' },
  { label: '项目', path: '/projects/' },
  { label: '归档', path: '/archive/' },
  { label: '关于', path: '/about/' },
];
