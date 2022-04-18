import pygame
import os
import random

# ���� ��θ� ���� ���� ������� ������ �ִٸ� �����
os.system("python /home/pi/webapps/music_play/stop_music.py")

# ���� ��θ� ���� ���� �÷��̸���Ʈ�� ���� �Ǿ� �ִ� ���ǵ��� list ���·� �����´�
path = "/home/pi/music_list/"
music_list = os.listdir(path)

# ���� ����� ���� ���� ���� ����
numbers = [i for i in range(len(music_list))]
random.shuffle(numbers)

# ���� �÷��̸� ���� mixer init
pygame.mixer.init()

# ���� ���
for i in range(len(music_list)):
    # ��׶��� ����� ���� ����
    # ���μ��� id�� �����ϱ� ���� file control
    file_path = "/home/pi/id_saver.txt"

    # pygame.mixer ����
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.load(path + music_list[numbers[i]])
    pygame.mixer.music.play()

    # file�� ���� ���� ���� ��׶��� ��� ���� ���μ����� id�� �����Ѵ�
    f = open(file_path, "w")
    f.write(str(os.getpid()))
    f.close()

    # �ν��Ͻ��� �޸𸮿� ������ �� ���� �ε��ؼ� �����ϴ� ���� �ƴ϶�
    # ��Ʈ���� �������� ������ �ǽð����� �ε� �ϸ鼭 ó���Ѵ�
    while pygame.mixer.music.get_busy() == True:
        continue
