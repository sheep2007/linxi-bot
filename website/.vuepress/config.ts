import { defineUserConfig } from "vuepress";
import type { DefaultThemeOptions } from "vuepress";
import recoTheme from "vuepress-theme-reco";

export default defineUserConfig({
  title: "林汐 · 文档",
  description: "林汐Bot的使用与开发文档",
  theme: recoTheme({
    style: "@vuepress-reco/style-default",
    logo: "/logo.png",
    author: "mute.",
    authorAvatar: "/head.png",
    docsRepo: "https://github.com/mute23-code/linxi-bot",
    docsBranch: "master",
    docsDir: "website",
    lastUpdatedText: "",
    // series 为原 sidebar
    series: {
      '/blogs/about/': [
        'introduce.md',
        'about',
        'contribute'  
      ],
      '/docs/module/bilibili/': [
        "base.md",
        "action",  
        "follow_up",
        "anchor",
        "anime",
        "list",
        "hot"
      ],
    },
    navbar: [
      { text: '主页', link: '/docs/index.html', icon: 'Home'},
      { text: '功能', link: '/docs/module.md', icon: 'Document'},
      {
        text: '开发',
        icon: 'Document',
        children: [
          {
            text: '前言',
            children: [
              { text: '前言', link: '#'},
              { text: '准备工作', link: '#'}
            ]
          },
          {
            text: '安装',
            children: [
              { text: '安装林汐Bot', link: '#' },
              { text: '安装go-cqhttp', link: '#'},
            ],
          },
          {
            text: '配置',
            children: [
              { text: '环境配置', link: '#'},
              { text: '林汐Bot配置', link: '#'}
            ]
          },
          {
            text: '部署',
            children: [
              { text: 'Docker部署', link: '#' }
            ]
          }
        ]
      },
      { text: '关于',
        children: [
          { text: '关于', link: '/blogs/about/introduce.md' },
          { text: '反馈', link: 'https://support.qq.com/product/426080' },
          { text: '赞助', link: 'https://afdian.net/a/linxi-bot' }
        ]
      },
      { text: '留言板', link: '/blogs/message-board.html', icon: 'Chat'},
      { text: '时间轴', link: '/timeline/'}
    ],
    bulletin: {
      body: [
        {
          type: "text",
          content: `🎉🎉🎉 林汐先已经接近 1.0 版本，在发布 1.0 版本之前不会再有大的更新，大家可以尽情尝鲜了，并且希望大家在 QQ 群和 GitHub 踊跃反馈使用体验，我会在第一时间响应。`,
          style: "font-size: 12px;",
        },
        {
          type: "hr",
        },
        {
          type: "title",
          content: "QQ 群",
        },
        {
          type: "text",
          content: `
          <ul>
            <li>QQ群：413820772</li>
          </ul>`,
          style: "font-size: 12px;",
        },
        {
          type: "hr",
        },
        {
          type: "title",
          content: "GitHub",
        },
        {
          type: "text",
          content: `
          <ul>
            <li><a href="https://github.com/mute23-code/linxi-bot/issues">Issues<a/></li>
            <li><a href="https://github.com/mute23-code/linxi-bot/discussions/1">Discussions<a/></li>
          </ul>`,
          style: "font-size: 12px;",
        },
        {
          type: "hr",
        },
        {
          type: "buttongroup",
          children: [
            {
              text: "打赏",
              link: "https://afdian.net/a/linxi-bot",
            },
          ],
        },
      ],
    },
    // valineConfig 配置与 1.x 一致
    commentConfig: {
      type: 'valine',
      options: {
        appId: 'Wwr4rGsCAurIttBF4d4rCq7e-gzGzoHsz', // your appId
        appKey: '99cVtaoPMWZ2ziaCvgnk8UNS', // your appKey
        placeholder: '填写邮箱可以收到回复提醒哦！',
        verify: true, // 验证码服务
        hideComments: true, // 全局隐藏评论，默认 false
        recordIP: true,
      }
    },
  }),
  // debug: true,
});
