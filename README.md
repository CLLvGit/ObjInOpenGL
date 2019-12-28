# ObjInOpenGL
计算机图形学 PJ2 编程画一个真实感静态景物 \
吕承亮 16307130144 \
\
**程序说明** 
1. 运行方法 \
    运行./dist目录下的可执行程序 FileChooseGUI.exe。在弹出的界面中，点击“选择”按钮，选择一个obj格式的模型文件。点击开始，程序绘制选择的模型。\
    注： 1) 在resources文件夹下，有可用的示例模型
        2) 使用鼠标滚轮，可以缩放显示的模型
2. 开发环境 \
    使用python2.7开发 \
    主要的第三方库有：
    1) OpenGL，用于渲染图像
    2) pygame，用于读取贴图文件
3. 程序实现原理
    1) 根据obj文件的格式，读入模型数据，生成图像面信息和贴图信息
    2) 根据已读数据，使用OpenGL绘制图形
    3) 使用OpenGL提供的回调函数，根据鼠标滚轮的输入调整模型大小，根据时间调整模型的旋转角度
