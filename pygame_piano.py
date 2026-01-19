import pygame
import os

# Pygameの初期化
pygame.init()
pygame.mixer.init()

# 画面サイズ
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 600
FPS = 60

# 色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (30, 30, 30)
BLUE = (100, 150, 255)

class Key:
  """ピアノの鍵盤クラス"""

  def __init__(self, note, x, y, width, height, is_black=False):
    self.note = note
    self.rect = pygame.Rect(x, y, width, height)
    self.is_black = is_black
    self.is_pressed = False
    self.color = BLACK if is_black else WHITE
    self.original_color = self.color

  def draw(self, screen):
    """鍵盤を描画"""
    if self.is_pressed:
      # 押されている時は色を変更
      color = DARK_GRAY if self.is_black else LIGHT_GRAY
    else:
      color = self.original_color

    pygame.draw.rect(screen, color, self.rect)
    pygame.draw.rect(screen, BLACK, self.rect, 2)  # 枠線

  def is_clicked(self, pos):
    """クリック位置が鍵盤内かチェック"""
    return self.rect.collidepoint(pos)

  def play_sound(self):
    """音を再生"""
    filename = self.note.replace('#', 'b')
    sound_path = f'sounds/{filename}.wav'
    if os.path.exists(sound_path):
      sound = pygame.mixer.Sound(sound_path)
      sound.play()
    else:
      print(f"警告: {sound_path} が見つかりません")

class Piano:
  """ピアノアプリケーションクラス"""

  def __init__(self):
    self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("🎹 Pygame Piano")
    self.clock = pygame.time.Clock()
    self.running = True
    self.current_octave = 4  # C4から開始

    self.keys = []
    self.setup_keys()

    # キーマップ
    self.key_map_base = {
        pygame.K_a: 'C',
        pygame.K_s: 'D',
        pygame.K_d: 'E',
        pygame.K_f: 'F',
        pygame.K_g: 'G',
        pygame.K_h: 'A',
        pygame.K_j: 'B',
        pygame.K_w: 'C#',
        pygame.K_e: 'D#',
        pygame.K_t: 'F#',
        pygame.K_y: 'G#',
        pygame.K_u: 'A#',
        pygame.K_k: 'C5',  # C5専用
    }

  def setup_keys(self):
    """鍵盤を配置"""
    white_width = WINDOW_WIDTH // 14  # 14個の白鍵
    white_height = WINDOW_HEIGHT - 100
    black_width = white_width * 0.6
    black_height = white_height * 0.6

    # C4-B5の2オクターブ
    white_notes = ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4',
                   'C5', 'D5', 'E5', 'F5', 'G5', 'A5', 'B5']

    # 白鍵を配置
    for i, note in enumerate(white_notes):
      x = i * white_width
      key = Key(note, x, 50, white_width, white_height, is_black=False)
      self.keys.append(key)

    # 黒鍵を配置（C#, D#, F#, G#, A#）
    # 各オクターブの白鍵の配置: C D E F G A B
    # 黒鍵は以下の位置に来る:
    # C# = C と D の間 (C + 0.6の幅くらい)
    # D# = D と E の間
    # F# = F と G の間
    # G# = G と A の間
    # A# = A と B の間

    black_positions = [
        (0, 'C#4'),  # C4とD4の間
        (1, 'D#4'),  # D4とE4の間
        (3, 'F#4'),  # F4とG4の間
        (4, 'G#4'),  # G4とA4の間
        (5, 'A#4'),  # A4とB4の間
        (7, 'C#5'),  # C5とD5の間
        (8, 'D#5'),  # D5とE5の間
        (10, 'F#5'),  # F5とG5の間
        (11, 'G#5'),  # G5とA5の間
        (12, 'A#5'),  # A5とB5の間
    ]

    for white_index, note in black_positions:
      # 白鍵の右側に黒鍵を配置
      x = (white_index * white_width) + (white_width - black_width / 2)
      key = Key(note, x, 50, black_width, black_height, is_black=True)
      self.keys.append(key)

  def handle_events(self):
    """イベント処理"""
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        self.running = False

      # マウスクリック
      elif event.type == pygame.MOUSEBUTTONDOWN:
        # 黒鍵を先にチェック（黒鍵が優先）
        clicked = False
        for key in self.keys:
          if key.is_black and key.is_clicked(event.pos):
            key.is_pressed = True
            key.play_sound()
            clicked = True
            break

        # 黒鍵が反応しなかったら白鍵をチェック
        if not clicked:
          for key in self.keys:
            if not key.is_black and key.is_clicked(event.pos):
              key.is_pressed = True
              key.play_sound()
              break

      elif event.type == pygame.MOUSEBUTTONUP:
        for key in self.keys:
          key.is_pressed = False

      # キーボード入力
      elif event.type == pygame.KEYDOWN:
        if event.key in self.key_map_base:
          note_name = self.key_map_base[event.key]

          # K キーはC5固定
          if event.key == pygame.K_k:
            note = 'C5'
          # その他はShiftでオクターブを変更
          elif pygame.key.get_mods() & pygame.KMOD_SHIFT:
            note = note_name + '5'
          else:
            note = note_name + '4'

          # 対応する鍵盤を探して押す
          for key in self.keys:
            if key.note == note:
              key.is_pressed = True
              key.play_sound()
              break

      elif event.type == pygame.KEYUP:
        for key in self.keys:
          key.is_pressed = False

  def draw(self):
    """画面に描画"""
    self.screen.fill(GRAY)

    # 白鍵を先に描画
    for key in self.keys:
      if not key.is_black:
        key.draw(self.screen)

    # 黒鍵を後に描画（白鍵の上に見える）
    for key in self.keys:
      if key.is_black:
        key.draw(self.screen)

    # UI情報
    font = pygame.font.Font(None, 24)
    octave_text = font.render("Shift + キーでオクターブ変更 | K = C5", True, WHITE)
    self.screen.blit(octave_text, (20, 10))

    pygame.display.flip()

  def run(self):
    """メインループ"""
    while self.running:
      self.handle_events()
      self.draw()
      self.clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
  piano = Piano()
  piano.run()
