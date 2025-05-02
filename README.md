# 企业信誉评估系统 (Enterprise Credit Evaluation System)

## 项目概述

企业信誉评估系统是一个基于Django开发的Web应用，旨在帮助用户评估和分析企业的信誉状况。系统通过分析企业的执行情况、案件数量、涉案金额和判决情况等多维度数据，为用户提供企业信誉的综合评分，帮助用户更好地了解企业的风险状况。

## 主要功能

- **用户认证**: 支持用户注册、登录和个人资料管理
- **企业搜索**: 通过企业名称快速查找企业信息
- **高级筛选**: 支持多维度条件筛选企业数据
- **企业详情**: 展示企业的详细信息，包括基本信息和信誉相关数据
- **信誉评分**: 基于多维度数据计算企业信誉评分
- **收藏功能**: 允许用户收藏感兴趣的企业，方便后续查看
- **权重设置**: 用户可以自定义评分维度的权重，获得个性化的企业评分
- **管理后台**: 提供完善的后台管理功能，支持用户管理等操作

## 技术栈

- **后端框架**: Django 5.1.4
- **数据库**: MySQL
- **前端框架**: Bootstrap 5
- **数据可视化**: 使用图表展示企业评分数据
- **用户认证**: 基于Django内置认证系统
- **响应式设计**: 支持多种设备访问

## 安装说明

### 前提条件

- Python 3.9+
- MySQL 5.7+
- pip (Python包管理工具)

### 安装步骤

1. 克隆项目代码:
   ```
   git clone https://github.com/yourusername/enterprise-credit-evaluation.git
   cd enterprise-credit-evaluation
   ```

2. 创建并激活虚拟环境:
   ```
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/MacOS
   source venv/bin/activate
   ```

3. 安装依赖包:
   ```
   pip install -r requirements.txt
   ```

4. 修改数据库配置:
   在 `djangoProject/settings.py` 中配置数据库连接信息

5. 执行数据库迁移:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

6. 创建超级用户:
   ```
   python manage.py createsuperuser
   ```

7. 运行开发服务器:
   ```
   python manage.py runserver
   ```

8. 访问系统:
   - 前台: http://127.0.0.1:8000/
   - 后台: http://127.0.0.1:8000/admin/

## 系统截图

*(未来可以在这里添加系统界面截图)*

## 数据说明

系统主要使用以下数据维度计算企业信誉评分:

- **执行情况**: 企业的执行记录数量
- **案件数量**: 企业涉及的案件数量
- **涉案金额**: 企业涉及案件的总金额
- **判决情况**: 企业相关的判决记录数量

每个维度的权重默认为25%，用户可以根据自己的需求调整权重。

## 开发团队

*(在这里添加开发团队信息)*

## 许可证

该项目基于MIT许可证开源。

## 联系方式

*(在这里添加联系方式)* 