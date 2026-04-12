import pyautogui as pa
import cv2
import tkinter as tk
import numpy as np
import time

# 核心函数
# 截屏并识别图像，返回坐标/空值
def find_screen(template_path, threshold=0.8):
    template = cv2.imread(template_path, cv2.IMREAD_COLOR)
    if template is None:
        print(f"错误：无法读取模板图像 {template_path}")
        return None
    screen = np.array(pa.screenshot())
    screen = cv2.cvtColor(screen, cv2.COLOR_RGB2BGR)
    result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    if max_val >= threshold:
        h, w, _ = template.shape
        top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)
        center_x = top_left[0] + w // 2
        center_y = top_left[1] + h // 2
        return center_x, center_y, w, h
    else:
        return None


def check_color_in_region(screen, top_left, target_rgb_range, offset=(0, 0)):
    # 计算校验点坐标（基于左上角+偏移）
    check_x = top_left[0] + offset[0]
    check_y = top_left[1] + offset[1]

    # 确保坐标在屏幕范围内
    h, w = screen.shape[:2]
    if not (0 <= check_x < w and 0 <= check_y < h):
        print("校验点超出屏幕截图范围")
        return False

    # 提取BGR颜色（OpenCV默认BGR，需转为RGB）
    b, g, r = screen[check_y, check_x]
    rgb_color = (r, g, b)
    print(f"\n校验点颜色：RGB{rgb_color}")

    # 检查是否在目标范围内
    (min_r, min_g, min_b), (max_r, max_g, max_b) = target_rgb_range
    return (min_r <= rgb_color[0] <= max_r and
            min_g <= rgb_color[1] <= max_g and
            min_b <= rgb_color[2] <= max_b)


def click_if_color_matches(template_path, target_rgb_range, threshold=0.8, max_retry=10, color_check_offset=(0, 0)):
    try:
        retry_count = 0
        location = None
        # 循环查找目标
        while not location and retry_count < max_retry:
            location = find_screen(template_path, threshold)
            if not location:
                retry_count += 1
                print(f"\r第 {retry_count} 次未找到目标", end='')
                time.sleep(2)

        if not location:
            print(f"\n超过最大重试次数，未找到 {template_path}")
            return

        center_x, center_y, w, h = location
        top_left = (center_x - w // 2, center_y - h//2)
        # 获取当前屏幕截图（用于颜色校验）
        screen = np.array(pa.screenshot())
        screen_bgr = cv2.cvtColor(screen, cv2.COLOR_RGB2BGR)  # 转为BGR格式

        # 检查颜色是否匹配
        color_matched = check_color_in_region(screen_bgr, top_left, target_rgb_range, color_check_offset)

        if color_matched:
            pa.click(center_x, center_y, button='left')
            print(f"\n颜色匹配，已点击目标（中心坐标：({center_x},{center_y})）")
            return True
        else:
            print(f"\n颜色不匹配，未执行点击")
            return False

    except Exception as e:
        print(f"\n操作失败：{str(e)}")



# 图片点击
def click_on_image(template_path, check_after_click=True, assign_template_path=None, threshold=0.8):
    # 查找
    retry_count = 0
    location = find_screen(template_path, threshold)
    while not location:
        retry_count += 1
        print(f"\r第 {retry_count} 次未查找到",end='')
        time.sleep(5)
        location = find_screen(template_path, threshold)

    # 点击
    x, y = location[:2]
    total_click_count = 0
    check_post = assign_template_path if assign_template_path is not None else template_path
    print()

    while True:
        pa.click(x, y, button='left')
        total_click_count += 1
        print(f"\r已点击 {template_path}（第 {total_click_count} 次）",end='')

        # 校验是否响应
        if not check_after_click:
            break

        time.sleep(0.8)
        post_check = find_screen(check_post, threshold)
        if assign_template_path is not None and post_check is not None:
            print(f"{template_path}（已查找{retry_count * 5} 秒）", end='')
            break
        elif not assign_template_path and not post_check:
            print(f"{template_path}（已查找{retry_count * 5} 秒）", end='')
            break






#荒原
def manor():

    v("荒原")
    #打开荒原
    click_on_image('./pic/manor.png')
    time.sleep(10)

    #尘微与厘
    click_on_image('./pic/experience.png', False)
    time.sleep(5)
    click_on_image('./pic/coin.png', False)
    time.sleep(5)

    #好感
    click_on_image('./pic/opinion.png')
    time.sleep(5)

    #工厂
    #收取
    click_on_image('./pic/pro.png', assign_template_path='./pic/gain.png')
    time.sleep(5)

    click_on_image('./pic/gain.png', False)
    time.sleep(5)

    #关闭获取界面
    pa.click(button='right')
    time.sleep(3)

    click_on_image('./pic/rest.png')
    time.sleep(3)

    click_on_image('./pic/redact.png')
    time.sleep(2)

    # 休息安置
    click_on_image('./pic/remove.png', False)
    time.sleep(0.8)
    #工作魔精的位置
    pa.click(1020, 900, 6, 0.8)
    time.sleep(1)
    click_on_image('./pic/house2.png', False)
    time.sleep(1)
    click_on_image('./pic/remove.png', False)
    time.sleep(0.8)
    # 工作魔精的位置
    pa.click(1320, 900, 2, 0.8)
    time.sleep(1)

    pa.click(button='middle')
    time.sleep(1)

    click_on_image('./pic/production.png')
    time.sleep(1.5)

    click_on_image('./pic/batchpro.png')
    time.sleep(1.5)

    click_on_image('./pic/batchput.png', False)
    time.sleep(1.5)

    click_on_image('./pic/batchmojing.png')
    time.sleep(2)


    pa.moveTo(468, 713)
    pa.mouseDown(button='left')
    pa.dragTo(1088, 713, duration=2)
    pa.moveTo(1500, 498)
    pa.dragTo(468, 498, duration=2)
    pa.mouseUp(button='left')
    time.sleep(3)

    pa.click(button='middle', clicks=3, interval=2.5)
    time.sleep(1.5)
    menu()
    print("荒原已完成")


#心相
def xinxiang():

    v("心相")
    #进入
    click_on_image('./pic/entrance.png')
    time.sleep(2)

    click_on_image('./pic/resource.png', assign_template_path='./pic/volition.png')
    time.sleep(2)

    click_on_image('./pic/volition.png')
    time.sleep(2)

    click_on_image('./pic/volition07.png', assign_template_path='./pic/letsgo.png')
    time.sleep(2)

    click_on_image('./pic/letsgo.png')
    time.sleep(5)

    #开始战斗
    click_on_image('./pic/4re.png')
    time.sleep(25)

    click_on_image('./pic/victory.png')
    time.sleep(5)

    # 返回主界面
    menu()
    print("心相已完成")


def gold(loop=False):

    # count = 0
    def run_gold(circulation=False):
        # nonlocal count
        # count += 1
        v("金币")
        # 进入
        click_on_image('./pic/entrance.png')
        time.sleep(2)
        click_on_image('./pic/resource.png', assign_template_path='./pic/gcoin.png')
        time.sleep(2)
        # 选择关卡
        click_on_image('./pic/gcoin.png')
        time.sleep(2)
        click_on_image('./pic/gcoin06.png', assign_template_path='./pic/letsgo.png')
        time.sleep(2)
        click_on_image('./pic/letsgo.png')
        time.sleep(5)

        # 开始战斗
        if circulation:
            fight(judge_picture="./pic/active.png", circulation=True)
        else:
            #单次战斗 默认两次
            fight(2, judge_picture="./pic/active.png")


    # 循环执行判断
    if loop:
        run_gold(True)
        print("金币循环已退出")
    else:
        # 单次执行
        run_gold()
        print("金币已完成")

    # 返回主界面
    menu()




def mote(loop=False):

    def run_mote(circulation=False):
        v("微尘")
        # 进入
        click_on_image('./pic/entrance.png')
        time.sleep(2)
        click_on_image('./pic/resource.png', assign_template_path="./pic/mote.png")
        time.sleep(2)
        #微尘
        click_on_image("./pic/mote.png")
        time.sleep(2)
        click_on_image('./pic/mote06.png', assign_template_path='./pic/letsgo.png')
        time.sleep(2)
        click_on_image('./pic/letsgo.png')
        time.sleep(5)

        # 开始战斗
        if circulation:
            fight(judge_picture="./pic/active.png", circulation=True)
        else:
            # 单次战斗 默认两次
            fight(2, judge_picture="./pic/active.png")

    # 循环执行判断
    if loop:
        run_mote(True)
        print("微尘循环已退出")
    else:
        # 单次执行
        run_mote()
        print("微尘已完成")

    # 返回主界面
    menu()




#材料(未更新)
def chapter4act21():

    v("421")
    #进入
    click_on_image('./pic/entrance.png')
    time.sleep(2)

    #拖动
    pa.mouseDown(200,520,button="left")
    pa.dragTo(1730,520,duration=3)
    pa.mouseUp(button="left")
    time.sleep(2)

    #章节
    click_on_image('./pic/chapter4.png')
    time.sleep(2)

    #拖动
    pa.mouseDown(200, 820, button="left")
    pa.dragTo(1730, 820, duration=3)
    pa.mouseUp(button="left")
    time.sleep(2)

    #21
    click_on_image('./pic/421.png')
    time.sleep(2)

    #厄运
    pa.click(1630,400,1,duration=1)
    time.sleep(2)

    click_on_image('./pic/misgo.png')
    time.sleep(5)

    #开始战斗
    click_on_image('./pic/4re.png')
    time.sleep(40)

    click_on_image('./pic/victory.png')
    time.sleep(5)

    #返回主界面
    menu()
    print("421已完成")



#唱片机
def record_player():

    v("唱片机")
    location = find_screen('./pic/record_assistance.png',)
    x, y = location[:2]
    pa.click(x+176,y,2)
    time.sleep(3)

    # 进入判断
    estimate1 = find_screen('./pic/record.png')
    if estimate1:
        # click_on_image('./pic/record.png')
        # time.sleep(2)

        estimate2 = find_screen('./pic/check_rerecord.png', )
        if estimate2:
            # 返回主界面
            menu()
            print("唱片机已领取")
        else:
            # 领取
            click_on_image('./pic/rerecord.png')
            time.sleep(7)
            # 返回主界面
            menu()
            print("唱片机已领取")
    else:
        return


#任务
def task():

    v("任务")
    # 进入
    click_on_image('./pic/task.png')

    #日常领取
    click_on_image('./pic/allre.png')
    time.sleep(3)
    pa.click(button='right')

    #周常领取
    click_on_image('./pic/weekact.png', False)
    time.sleep(3)
    estimate1 = find_screen('./pic/weekre.png')
    while estimate1:
        click_on_image('./pic/weekre.png')
        time.sleep(3)
        pa.click(button='right')
        time.sleep(1)
        estimate1 = find_screen('./pic/weekre.png')
    # 返回主界面
    menu()
    print("任务已领取")

    # # 像素颜色识别点击功能
    # # 257，25
    # estimate = click_if_color_matches(
    #     template_path="pic/weekact.png",  # 按钮模板图片
    #     target_rgb_range=((180, 0, 0), (255, 100, 100)),
    #     threshold=0.8,
    #     max_retry=50,
    #     color_check_offset=(257, 25)
    # )
    # if estimate:
    #     time.sleep(1)
    #     click_on_image('./pic/allre.png')
    #     time.sleep(5)
    #     pa.click(button='right')
    #     time.sleep(3)
    #     # 返回主界面
    #     menu()
    #     print("任务已领取")
    # else:
    #     # 返回主界面
    #     menu()
    #     print("任务已领取")



#活动
def timed_event():

    v("活动")
    #活动模块
    wherego()
    # calaite()
    # event_simulate()

    # 返回主界面
    menu()
    print("活动关卡结束")



#人们向何处去
def wherego():
    # 进入
    click_on_image('./opic/eventplot_wherego.png')
    click_on_image('./opic/event_wherego.png')
    click_on_image("./opic/chapter_wherego.png", assign_template_path="./opic/actletsgo_wherego.png")
    click_on_image("./opic/actletsgo_wherego.png")
    # 开始战斗
    fight(3, judge_picture="./pic/active.png")


#绿松石蛇俱乐部
def calaite():
    # 进入
    click_on_image('./opic/eventplot_calaite.png')
    click_on_image('./opic/event_calaite.png')
    click_on_image("./opic/chapter_calaite.png", assign_template_path="./opic/actletsgo_calaite.png")
    click_on_image("./opic/actletsgo_calaite.png")
    # 开始战斗
    fight(3, judge_picture="./pic/active.png")


#雨中漫游指南
def event_simulate():
    for i in range(1999):
        click_on_image('./opic/simulate_start.png')
        click_on_image('./opic/simulate_next.png')
        click_on_image('./opic/simulate_select.png')
        back_discern('./opic/simulate_confirm.png')
        click_on_image('./opic/simulate_confirm.png')
        back_discern('./opic/simulate_end.png', 'middle')
        click_on_image('./opic/simulate_end.png')
        click_on_image('./pic/confirm.png')
        back_discern('./opic/simulate_start.png',clicks=5)


#单一对象返回识别循环
def back_discern(judge_picture,click='right',clicks=1):
    judge = None
    while not judge:
        pa.click(clicks=clicks,interval=0.75,button=click)
        time.sleep(1.5)
        judge = find_screen(judge_picture)

# 返回主界面
def menu():
    back_discern('./pic/menu.png')
    # judge = None
    # while not judge:
    #     pa.click(button='right')
    #     time.sleep(2)
    #     judge = find_screen('./pic/menu.png')
    print("返回主界面")


#战斗循环
def fight(x=1, judge_picture=None, circulation=False):
    judge = False if judge_picture else True

    def f():
        nonlocal judge
        # 战斗
        click_on_image('./pic/re.png')
        if judge_picture:
            judge = find_screen(judge_picture)
            if judge:
                pa.click(button='middle')
                print("活性不足")
                time.sleep(1)
                return judge
        time.sleep(15)
        click_on_image('./pic/victory.png', assign_template_path='./pic/re.png')
        time.sleep(1)
        print("此次战斗结束")

    if circulation:
        if not judge_picture:
            print("未指定结束标识")
            return
        #启动循环
        judge = False
        while not judge:
            f()
    else:
        for i in range(x):
            f()
            if judge and judge_picture:
                break


#获取选中状态
def get_selected_modules():
    selected = []
    for key, var in selected_modules.items():
        if var.get():
            selected.append(key)
    return selected

#总开关
def start_select(selected_modules):
    selected = get_selected_modules()
    print("选中的模块：", selected)
    b7.config(state="disabled") # 禁用按键

    if selected_modules["manor"].get():
        manor()
    if selected_modules["xinxiang"].get():
        xinxiang()
    if selected_modules["act"].get():
        timed_event()
    if selected_modules["gold_re"].get():
        gold(loop=True)
    if selected_modules["mote_re"].get():
        mote(loop=True)
    if selected_modules["gold"].get():
        gold()
    if selected_modules["mote"].get():
        mote()
    if selected_modules["record_player"].get():
        record_player()
    if selected_modules["task"].get():
        task()

    # if selected_modules["421"].get() == True:
    #     chapter4act21()
    if selected_modules["fight"].get():
        fight(judge_picture="./pic/active.png", circulation=True)

    v("已完成")
    print("选中已全部完成")
    b7.config(state="normal") #恢复按键

    for key in selected:
        selected_modules[key].set(False)



#UI窗口
root = tk.Tk()
root.title("重返未来：1999 日常自动")
root.geometry("400x550+50+40")
font_config = ("SimHei", 10)


# 标签刷新
def v(name):
    var = name
    label.config(text=f"正在进行：{var}")
    root.update()


# 模块选择区域
## 模块名称映射
module_mapping = {
    "manor": "荒原",
    "xinxiang": "心相",
    "gold": "金币",
    "mote": "微尘",
    "act": "活动",
    "record_player": "唱片机",
    "task": "任务",
    "gold_re": "金币循环",
    "mote_re": "微尘循环",
    "fight": "战斗循环"

    # "421": "421"
}

## 初始化选中状态的字典
selected_modules = {key: tk.BooleanVar() for key in module_mapping.keys()}

# selected_modules = {
#                     "manor": tk.BooleanVar(),
#                     "xinxiang": tk.BooleanVar(),
#                     "gold": tk.BooleanVar(),
#                     "mote": tk.BooleanVar(),
#                     "act": tk.BooleanVar(),
#                     "record_player": tk.BooleanVar(),
#                     "task":tk.BooleanVar(),
#                     "gold_re": tk.BooleanVar(),
#                     "mote_re": tk.BooleanVar(),
#
#                     "fight": tk.BooleanVar(),
#                      #"421": tk.BooleanVar()
#                     }

frame_modules = tk.Frame(root)
frame_modules.pack(pady=10, padx=20, fill="x")

## 循环创建复选框
for key, text in module_mapping.items():
    cb = tk.Checkbutton(
        frame_modules,
        text=text,
        variable=selected_modules[key],
        font=font_config
    )
    cb.pack(anchor="center", pady=2)

# tk.Checkbutton(frame_modules, text="荒原", variable=selected_modules["manor"], font=font_config).pack(anchor="center", pady=2)
# tk.Checkbutton(frame_modules, text="心相", variable=selected_modules["xinxiang"], font=font_config).pack(anchor="center", pady=2)
# tk.Checkbutton(frame_modules, text="金币", variable=selected_modules["gold"], font=font_config).pack(anchor="center", pady=2)
# tk.Checkbutton(frame_modules, text="微尘", variable=selected_modules["mote"], font=font_config).pack(anchor="center", pady=2)
# tk.Checkbutton(frame_modules, text="活动", variable=selected_modules["act"], font=font_config).pack(anchor="center", pady=2)
# tk.Checkbutton(frame_modules, text="唱片机", variable=selected_modules["record_player"], font=font_config).pack(anchor="center", pady=2)
# tk.Checkbutton(frame_modules, text="任务", variable=selected_modules["task"], font=font_config).pack(anchor="center", pady=2)
# tk.Checkbutton(frame_modules, text="金币循环", variable=selected_modules["gold_re"], font=font_config).pack(anchor="center", pady=2)
# tk.Checkbutton(frame_modules, text="微尘循环", variable=selected_modules["mote_re"], font=font_config).pack(anchor="center", pady=2)
# tk.Checkbutton(frame_modules, text="战斗循环", variable=selected_modules["fight"], font=font_config).pack(anchor="center", pady=2)


#标签
label = tk.Label(root, text=' ', font=("Arial", 14))
label.pack(pady=20)


#按钮
b7 = tk.Button(root, text="开始执行", width=20, height=3, command=lambda: start_select(selected_modules))
b7.pack()


# 进入消息循环
root.mainloop()

