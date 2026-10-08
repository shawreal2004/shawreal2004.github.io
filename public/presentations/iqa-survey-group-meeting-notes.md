# 图像质量评价：我的理解与课题思考

作者：shaw chenyu

正文汇报为第 1–18 页，附录为第 19–21 页。配图与构造分数均用于教学，研究设想尚未开展正式实验。

## 第 1 页：封面

各位老师、同学好，我是 shaw chenyu。本次汇报围绕两篇感知质量评价综述，重点讲我对 IQA 的理解，再结合 AIGC 与 UGC 混合的 VR 图片数据库和算法，说明目前形成的研究问题与下一步计划。现在还处于入门阅读阶段，没有正式数据库或算法实验结果。

出处：

Zhai, G.; Min, X. Perceptual image quality assessment: a survey. Science China Information Sciences, 2020, 63:211301. https://doi.org/10.1007/s11432-019-2757-1

Min, X.; Duan, H.; Sun, W.; Zhu, Y.; Zhai, G. Perceptual video quality assessment: a survey. Science China Information Sciences, 2024, 67:211301. https://doi.org/10.1007/s11432-024-4133-3

于翔旭老师新生进组学习计划，导师提供 PDF，26 页。§5.4–5.5，PDF 第 9 页。

配图：shaw 的手记入门百科中已有的自制教学示例。public/images/encyclopedia/figure-manifest.json 记录生成参数。图片不代表真实数据库、生成器输出或实验结果。

## 第 2 页：阅读材料与本次汇报范围

两篇综述的侧重点不同。IQA 综述帮助我建立数据库、主观评价、客观方法与模型评测之间的联系。VQA 综述补充时间因素、显示条件和 VR 观看行为。我目前以全景静态图片为研究对象，因此只迁移相关的评测思想，不把视频方法直接作为图片算法。导师教程进一步强调可复现的实验习惯。我的收获是先明确评价目标和标签，再选择方法和比较协议，而不是只记算法名称。

出处：

Zhai, G.; Min, X. Perceptual image quality assessment: a survey. Science China Information Sciences, 2020, 63:211301. https://doi.org/10.1007/s11432-019-2757-1
重点：§2、§3、§4.11、§5。

Min, X.; Duan, H.; Sun, W.; Zhu, Y.; Zhai, G. Perceptual video quality assessment: a survey. Science China Information Sciences, 2024, 67:211301. https://doi.org/10.1007/s11432-024-4133-3
重点：§2.1、§4.4、§5。

于翔旭老师新生进组学习计划，导师提供 PDF，26 页。§5.4–5.5，PDF 第 9 页。

## 第 3 页：我对 IQA 的理解

我的理解是，感知质量评价希望预测人在规定条件下对图像的质量判断。图像像素是输入，评分问题、观察者和展示条件决定标签含义。比如同一张全景图，桌面展开图、可交互视口与头显浏览会有不同的可见细节和观看体验。因此建库时必须写清楚怎样看、评什么。整体视觉质量、美感、内容是否符合提示词、眩晕等体验指标可能相关，但各有定义，不能把它们混成一个没有解释的分数。

出处：

Zhai, G.; Min, X. Perceptual image quality assessment: a survey. Science China Information Sciences, 2020, 63:211301. https://doi.org/10.1007/s11432-019-2757-1
§1–2，主观评价与人类视觉系统。

Min, X.; Duan, H.; Sun, W.; Zhu, Y.; Zhai, G. Perceptual video quality assessment: a survey. Science China Information Sciences, 2024, 67:211301. https://doi.org/10.1007/s11432-024-4133-3
§2.1，主观测试方法与条件。

## 第 4 页：FR、RR 与 NR 的区别

这三个类别区分推理时参考信息的可用程度。FR 可以获得完整高质量参考，例如原始全景与其压缩版本。RR 使用有限参考特征。NR 只依靠待评价内容，是我当前拟采用的起点。无参考不等于无监督，NR 模型训练时常需要 MOS 标签。提示词是生成条件，不是可以直接计算逐像素误差的高质量参考图。同一场景下的不同生成图若未建立可信对应关系，也不能自动拿来作为 FR 参考。

出处：

Zhai, G.; Min, X. Perceptual image quality assessment: a survey. Science China Information Sciences, 2020, 63:211301. https://doi.org/10.1007/s11432-019-2757-1
§3，PDF p.9–22。

## 第 5 页：模糊与噪声的观察线索

我首先需要学会观察失真。模糊通常削弱边缘和高频细节，噪声是叠加的随机波动，它可能让图像看起来更有高频变化，但这不意味着质量更好。这里两组分别使用相同输入，对比未添加失真的示意图和高斯变化。它们只解释现象，不代表真实数据，也没有 MOS 标签。实际拍摄与压缩可能同时引入多种失真，不能简单依赖一个锐度值给整体质量打分。

说明：高斯模糊 σ=1.5 px，高斯噪声 σ=20（8 bit），自制示意场景；不是主观实验。

出处：

Zhai, G.; Min, X. Perceptual image quality assessment: a survey. Science China Information Sciences, 2020, 63:211301. https://doi.org/10.1007/s11432-019-2757-1
§2 数据库失真类型，§3.3.1 失真专用 NR 方法。

配图：shaw 的手记入门百科中已有的自制教学示例。public/images/encyclopedia/figure-manifest.json 记录生成参数。图片不代表真实数据库、生成器输出或实验结果。

## 第 6 页：伪影与处理链

伪影是采集、编码、重建或处理带来的额外结构，常见表现包括压缩块、振铃、色带和锯齿。这里 JPEG 图使用实际低质量编码再解码，振铃图则只是边缘波纹的解析示意。我的课题需要同时记录产生这些现象的处理链，例如全景拼接、投影重采样和平台压缩。ERP 的极区拉伸是投影几何特征，不能直接当作质量缺陷。接缝断裂或重采样造成的额外失真才需要按具体观看条件评价。

说明：JPEG quality=5；振铃为解析示意，色带以 32 级步长量化；这些示例没有质量标签。

出处：

Zhai, G.; Min, X. Perceptual image quality assessment: a survey. Science China Information Sciences, 2020, 63:211301. https://doi.org/10.1007/s11432-019-2757-1
§2 失真类型，§3.1 与 §3.3。

配图：shaw 的手记入门百科中已有的自制教学示例。public/images/encyclopedia/figure-manifest.json 记录生成参数。图片不代表真实数据库、生成器输出或实验结果。

## 第 7 页：IQA 方法及其假设

综述使我意识到，方法选择需要看它依赖什么假设。PSNR 衡量相对参考的像素误差，SSIM 使用局部亮度、对比度和结构相似性，都需要合适参考。NSS 方法利用自然场景统计规律，BRISQUE 与 NIQE 的训练方式并不相同。学习方法从局部或整体特征中预测质量，效果依赖数据、标签和预训练。在生成内容和 ERP 图片中，自然图像统计先验是否仍适用需要验证。方法名称多不等于理解充分，我要能解释输入、监督与汇聚方式。

出处：

Zhai, G.; Min, X. Perceptual image quality assessment: a survey. Science China Information Sciences, 2020, 63:211301. https://doi.org/10.1007/s11432-019-2757-1
§3.1.1，PDF p.9–11；§3.3.2，PDF p.17–22。

## 第 8 页：MOS 与评分分歧

MOS 是多位观察者评分的平均值。平均分相同，可以对应一致意见，也可以对应明显分歧。图中四位观察者的评分完全是教学构造，不是确定实验人数的建议。我认为数据库应保存逐人评分、有效观察者处理和分歧信息，并用合适方法报告不确定性。正式实验前还要固定评分维度、设备、观看时长、起始朝向和随机化方式。若使用头显，必须同时考虑休息、舒适度和实验流程，具体方案应与导师及适用规范核对。

说明：教学分数 A=[3,3,3,3]，B=[1,1,5,5]，两组均值为 3；不是真实评分。

出处：

Zhai, G.; Min, X. Perceptual image quality assessment: a survey. Science China Information Sciences, 2020, 63:211301. https://doi.org/10.1007/s11432-019-2757-1
§2 主观数据库。

Min, X.; Duan, H.; Sun, W.; Zhu, Y.; Zhai, G. Perceptual video quality assessment: a survey. Science China Information Sciences, 2024, 67:211301. https://doi.org/10.1007/s11432-024-4133-3
§2.1，PDF p.4–6。

配图：shaw 的手记入门百科中已有的自制教学示例。public/images/encyclopedia/figure-manifest.json 记录生成参数。图片不代表真实数据库、生成器输出或实验结果。

## 第 9 页：VQA 综述对我的启发

视频评价需要考虑帧内质量、帧间运动、闪烁、帧率与时间汇聚，简单平均每一帧 IQA 并不足以覆盖所有视频现象。对我当前的静态全景课题，最有用的启发是评分依赖展示条件和观看过程。用户转头产生不同视口，是同一静态图片的浏览行为，并不等于原始内容变成视频。QoE 还涉及交互和不适等体验，因此本阶段要先定义图片质量标签，避免评价目标扩得太大。

出处：

Min, X.; Duan, H.; Sun, W.; Zhu, Y.; Zhai, G. Perceptual video quality assessment: a survey. Science China Information Sciences, 2024, 67:211301. https://doi.org/10.1007/s11432-024-4133-3
§2.1、§3、§4.4，PDF p.4–6、15–26、32–35。

## 第 10 页：我的课题对象与来源记录

导师给出的方向是 AIGC 与 UGC 混合的 VR 图片数据库和算法。我暂把混合理解为数据库同时包含两类来源，并不自动等于一张图内的像素融合。UGC 描述用户创作或上传，上传内容也可能包含 AI；因此建库要给出可执行的来源规则。采集内容记录拍摄与拼接链，生成内容记录生成器、条件和种子，AI 编辑内容额外记录母图与修改区域。来源是元数据，质量必须由统一评价协议产生，不能提前认定哪类更好。

说明：课题对象与来源分类是我的操作化草案，AI 编辑是否纳入需与导师确认。

出处：

于翔旭老师新生进组学习计划，导师提供 PDF，26 页。§5.4–5.5，PDF 第 9 页。

配图：shaw 的手记入门百科中已有的自制教学示例。public/images/encyclopedia/figure-manifest.json 记录生成参数。图片不代表真实数据库、生成器输出或实验结果。

## 第 11 页：清晰度之外的结构问题

生成图片可以边缘清楚，却存在连接关系、文字可读性或场景几何错误。这里椅腿图是人为绘制的现象示意，不能当作生成器输出或出现频率证据。我希望研究这些错误是否影响整体质量判断，但需要区分质量、结构合理性、提示词一致性与美感。风格化或超现实画面也不能默认低质。若标签把这些因素混在一起而没有说明，模型学习的目标会变得不清楚。是否采集辅助维度，要通过小规模预实验和导师讨论确定。

说明：结构图为人为绘制的教学示意；关于生成内容的评价维度是研究设想。

出处：

Zhai, G.; Min, X. Perceptual image quality assessment: a survey. Science China Information Sciences, 2020, 63:211301. https://doi.org/10.1007/s11432-019-2757-1
§4 特定应用中的质量定义。

配图：shaw 的手记入门百科中已有的自制教学示例。public/images/encyclopedia/figure-manifest.json 记录生成参数。图片不代表真实数据库、生成器输出或实验结果。

## 第 12 页：全景几何与观看视口

ERP 将球面展开为矩形，极区的像素密度较高。余弦纬度权重可以补偿球面面积，但并不表示人实际观看这些区域的概率。透视视口通过球面方向与相机投影获得，不能用 ERP 矩形裁剪直接替代。我需要检查偏航、俯仰、FOV、采样分辨率、插值与左右接缝环绕。图中视口来自方向场的实际投影，仅用于几何演示。当前可以先用固定视口保证可复现，之后再验证观看行为是否值得引入。

说明：方向场教学图，视口 330×174、水平 FOV 90°，采用双线性插值；不是真实场景数据。

出处：

Zhai, G.; Min, X. Perceptual image quality assessment: a survey. Science China Information Sciences, 2020, 63:211301. https://doi.org/10.1007/s11432-019-2757-1
§4.11，PDF p.33–34。

Min, X.; Duan, H.; Sun, W.; Zhu, Y.; Zhai, G. Perceptual video quality assessment: a survey. Science China Information Sciences, 2024, 67:211301. https://doi.org/10.1007/s11432-024-4133-3
§4.4.1，PDF p.32–33。

配图：shaw 的手记入门百科中已有的自制教学示例。public/images/encyclopedia/figure-manifest.json 记录生成参数。图片不代表真实数据库、生成器输出或实验结果。

## 第 13 页：数据库建设的初步方案

我认为先把数据库做得可解释，才有条件讨论模型改进。需要覆盖场景、来源、失真与质量范围，不能让 AIGC 与 UGC 同时对应两类完全不同场景或评分范围。元数据要保存文件哈希、内容家族、来源处理链、投影分辨率与显示条件。主观标签需要先做小规模预实验，看看评分问题是否明确、观察者是否能稳定作答。现在不设未经验证的数据库规模和实验人数，正式数量与协议由预实验、资源条件和导师意见确定。

说明：以下为拟建设方案，数据库尚未正式采集。

出处：

Zhai, G.; Min, X. Perceptual image quality assessment: a survey. Science China Information Sciences, 2020, 63:211301. https://doi.org/10.1007/s11432-019-2757-1
§2 与 §4.11。

Min, X.; Duan, H.; Sun, W.; Zhu, Y.; Zhai, G. Perceptual video quality assessment: a survey. Science China Information Sciences, 2024, 67:211301. https://doi.org/10.1007/s11432-024-4133-3
§2.1。

于翔旭老师新生进组学习计划，导师提供 PDF，26 页。§5.4–5.5，PDF 第 9 页。

## 第 14 页：内容家族与数据泄漏

这页对应导师教程第 5.5 节的第一条：避免相同 content 同时出现在训练和测试。全景图产生的不同方向视口不是独立内容，如果先提取视口再随机划分，就可能在训练中见到测试图的关联内容。我会先按内容家族划分，再在各集合内生成视口、失真版本和增强。内容家族还要检查同场景、母图、条件图以及近重复。生成随机种子和相似提示词是线索，不能单凭提示词相同就机械地认定是同一家族，仍需检查实际内容关系。

说明：图片为划分原则示意，不表示实际数据集划分结果。

出处：

于翔旭老师新生进组学习计划，导师提供 PDF，26 页。§5.4–5.5，PDF 第 9 页。

配图：shaw 的手记入门百科中已有的自制教学示例。public/images/encyclopedia/figure-manifest.json 记录生成参数。图片不代表真实数据库、生成器输出或实验结果。

## 第 15 页：我准备搭建的最小 NR 基线

我准备先完成可复现的小基线：固定视口采样，冻结现有图像编码器，汇聚视口特征，再训练轻量质量回归器。冻结编码器能够降低早期实验开销，但具体预训练模型与输入预处理还需核查。训练标签仍是全景的 MOS，不能把全局 MOS 当作每个局部视口都独立正确的标签。若一张图只有一个 MOS，我优先在汇聚之后监督全局预测。固定采样与均值汇聚只是可解释起点，不能提前断言已经适应全景与生成异常。

说明：仅为拟实现的基线，尚未训练或报告性能。

出处：

Zhai, G.; Min, X. Perceptual image quality assessment: a survey. Science China Information Sciences, 2020, 63:211301. https://doi.org/10.1007/s11432-019-2757-1
§3.3.2 与 §4.11。

于翔旭老师新生进组学习计划，导师提供 PDF，26 页。§5.4–5.5，PDF 第 9 页。

## 第 16 页：我怎样判断模型是否有效

IQA 模型不能只报告一个总体相关系数。SRCC 衡量排序关系，PLCC 衡量线性相关，RMSE 衡量分数误差，三者关注不同方面。标准基准有时进行非线性分数映射，需要说明映射在哪里拟合以及报告的是原始还是映射结果。测试集不能承担模型选型和调参。我会同时报告混合总体、来源内部和跨来源结果，保存散点图及失败样本。跨来源实验还要控制训练数量、场景与质量覆盖，否则下降未必由来源本身造成。

出处：

Zhai, G.; Min, X. Perceptual image quality assessment: a survey. Science China Information Sciences, 2020, 63:211301. https://doi.org/10.1007/s11432-019-2757-1
§5.1，PDF p.35–36。

于翔旭老师新生进组学习计划，导师提供 PDF，26 页。§5.4–5.5，PDF 第 9 页。

## 第 17 页：我想优先验证的研究问题

目前我有两个可以检验的想法。第一，同样数量的固定视口和针对缺陷区域的采样，是否会改变模型对局部异常的敏感性。第二，在相同图像特征上，增加能够反映结构异常的辅助信息，能否改善 AIGC 内部排序。两者都需要统一其他条件，并统计分来源失败案例。我还需要用来源元数据或简单来源预测作为诊断，检查模型是否主要利用来源平均分差。这里没有任何提升结论，只有研究问题，最终方案要由数据与预实验支持。

说明：以下均为待验证假设，未取得实验结果或证明新颖性。

出处：

Zhai, G.; Min, X. Perceptual image quality assessment: a survey. Science China Information Sciences, 2020, 63:211301. https://doi.org/10.1007/s11432-019-2757-1
§4.11，视口方法提供相关思路。

于翔旭老师新生进组学习计划，导师提供 PDF，26 页。§5.4–5.5，PDF 第 9 页。

## 第 18 页：下一步工作与组会讨论

这次阅读后，我最重要的收获是把质量目标、标签条件、方法假设和实验协议联系起来。下一步先明确混合来源与评价维度，再建立一小批可追溯样本和主观预实验，之后完成固定视口的 NR 基线，最后分析分来源结果与失败案例。想请老师帮助确认三点：是否纳入 AI 编辑图片，主标签只评价整体画质还是还要采集结构等维度，以及头显和现有数据资源能支持什么实验方案。这样的顺序能避免先设计复杂模型，再发现标签与任务定义不一致。

说明：当前是入门阶段计划，正式采集、模型训练与研究结论尚未完成。

出处：

于翔旭老师新生进组学习计划，导师提供 PDF，26 页。§5.4–5.5，PDF 第 9 页。

## 第 19 页：附录：相关性与数值误差

以三个构造样本说明指标差异：主观分数为 1、2、3，预测分数为 10、20、30。排序完全一致，且具有完全正线性关系，因此原始 SRCC 和 PLCC 都是 1，但原始 RMSE 为根号下 378，约 19.44。PLCC 高不表示分数落在相同量纲或数值准确。若采用映射后分数，必须把映射与评测协议说清楚。真实报告应同时提供原始或规定校准后的指标、散点图，并遵守固定评测划分。

说明：所有分数为构造教学数值，非模型实验结果。

出处：

Zhai, G.; Min, X. Perceptual image quality assessment: a survey. Science China Information Sciences, 2020, 63:211301. https://doi.org/10.1007/s11432-019-2757-1
§5.1，PDF p.35–36。

于翔旭老师新生进组学习计划，导师提供 PDF，26 页。§5.4–5.5，PDF 第 9 页。

## 第 20 页：附录：实验前后的核对清单

这份核对清单对应导师教程第 5.5 节，也结合了当前全景课题的细节。开始训练前，保存数据划分文件、随机种子、训练配置、预处理和预训练来源。正式比较中，保持同一测试集和评价协议，尽量与已有工作统一划分，重复关键实验。完成后保存每张图的预测、MOS 散点图、分来源指标和失败样本，并在条件允许时做跨数据集评价。对全景模型还需保存视口参数。预训练数据是否与测试集有内容重叠也应检查，不只是自己划分的训练集。

出处：

于翔旭老师新生进组学习计划，导师提供 PDF，26 页。§5.4–5.5，PDF 第 9 页。

## 第 21 页：参考材料与阅读定位

Zhai, G.; Min, X. Perceptual image quality assessment: a survey. Science China Information Sciences, 2020, 63:211301. https://doi.org/10.1007/s11432-019-2757-1

Min, X.; Duan, H.; Sun, W.; Zhu, Y.; Zhai, G. Perceptual video quality assessment: a survey. Science China Information Sciences, 2024, 67:211301. https://doi.org/10.1007/s11432-024-4133-3

于翔旭老师新生进组学习计划，导师提供 PDF，26 页。§5.4–5.5，PDF 第 9 页。

出处：

Zhai, G.; Min, X. Perceptual image quality assessment: a survey. Science China Information Sciences, 2020, 63:211301. https://doi.org/10.1007/s11432-019-2757-1

Min, X.; Duan, H.; Sun, W.; Zhu, Y.; Zhai, G. Perceptual video quality assessment: a survey. Science China Information Sciences, 2024, 67:211301. https://doi.org/10.1007/s11432-024-4133-3

于翔旭老师新生进组学习计划，导师提供 PDF，26 页。§5.4–5.5，PDF 第 9 页。

