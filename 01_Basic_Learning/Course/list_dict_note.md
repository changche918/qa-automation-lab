# Python List 與 Dict 完整筆記

> 給初階工程師的速查手冊，含爬蟲專案實戰範例

---

## 一、核心觀念一句話

| 資料結構 | 一句話記法 | 符號 |
|---------|-----------|------|
| **List（陣列）** | 用「位置」找資料，有順序 | `[ ]` 方括號 |
| **Dict（字典）** | 用「名字」找資料，像查字典 | `{ }` 大括號 |

---

## 二、List 陣列

### 2-1 建立 List

```python
# 空的 list
posts = []

# 有初始值的 list
forums = ['PTT', '巴哈', 'Dcard', 'Mobile01']

# 可以裝不同型別（但不建議，通常裝同類型）
mixed = [1, 'hello', True, 3.14]

# 用 list() 建立
numbers = list(range(5))   # [0, 1, 2, 3, 4]
```

### 2-2 存取元素（最重要）

```python
forums = ['PTT', '巴哈', 'Dcard', 'Mobile01']

# 用索引（從 0 開始）
print(forums[0])   # 'PTT'
print(forums[1])   # '巴哈'

# 負數索引（從後面數）
print(forums[-1])  # 'Mobile01'（最後一個）
print(forums[-2])  # 'Dcard'（倒數第二個）

# 切片 slicing [start:end:step]
print(forums[0:2])   # ['PTT', '巴哈']（不包含 index 2）
print(forums[:2])    # ['PTT', '巴哈']
print(forums[2:])    # ['Dcard', 'Mobile01']
print(forums[::-1])  # 反轉整個 list
```

### 2-3 修改、新增、刪除

```python
posts = ['文章A', '文章B', '文章C']

# 修改
posts[0] = '爆文A'

# 新增到尾端
posts.append('文章D')            # ['爆文A', '文章B', '文章C', '文章D']

# 插入到指定位置
posts.insert(1, '文章X')         # ['爆文A', '文章X', '文章B', ...]

# 合併另一個 list
posts.extend(['文章E', '文章F']) # 把兩個 list 接起來

# 刪除
posts.remove('文章B')            # 依「值」刪除第一個符合的
del posts[0]                    # 依「位置」刪除
last = posts.pop()              # 取出並移除最後一個
first = posts.pop(0)            # 取出並移除第一個
```

### 2-4 常用操作

```python
gp_scores = [50, 99, 30, 120, 80]

len(gp_scores)        # 5（長度）
max(gp_scores)        # 120
min(gp_scores)        # 30
sum(gp_scores)        # 379
sorted(gp_scores)     # [30, 50, 80, 99, 120]（回傳新的）
gp_scores.sort()      # 直接修改原本的 list

99 in gp_scores       # True（檢查是否存在）
gp_scores.count(99)   # 1（出現幾次）
gp_scores.index(99)   # 1（在哪個位置）
```

### 2-5 迴圈遍歷（爬蟲必用）

```python
posts = ['文章A', '文章B', '文章C']

# 基本遍歷
for post in posts:
    print(post)

# 同時拿到索引和值（超實用）
for i, post in enumerate(posts):
    print(f'第 {i+1} 篇：{post}')

# List comprehension（一行寫法，很 Python）
gp_scores = [50, 99, 30, 120, 80]
viral_scores = [gp for gp in gp_scores if gp >= 99]
# 結果：[99, 120]

# 把字串 list 全部轉成整數
str_nums = ['10', '20', '30']
nums = [int(n) for n in str_nums]  # [10, 20, 30]
```

---

## 三、Dict 字典

### 3-1 建立 Dict

```python
# 空的 dict
post = {}

# 有初始值（爬蟲最常見的結構）
post = {
    'title': '這是爆文標題',
    'gp': 99,
    'author': 'rc_dev',
    'is_viral': True
}

# 用 dict() 建立
post = dict(title='標題', gp=50)
```

### 3-2 存取元素

```python
post = {'title': '爆文', 'gp': 99, 'author': 'rc_dev'}

# 用 key 取值
print(post['title'])   # '爆文'
print(post['gp'])      # 99

# ⚠️ 如果 key 不存在，會噴 KeyError
# print(post['views'])  # KeyError!

# 安全取值：用 .get()（推薦）
print(post.get('views'))         # None（不會報錯）
print(post.get('views', 0))      # 0（指定預設值）
```

### 3-3 新增、修改、刪除

```python
post = {'title': '爆文', 'gp': 99}

# 新增或修改（語法一樣）
post['author'] = 'rc_dev'     # 新增
post['gp'] = 120              # 修改

# 刪除
del post['author']
gp = post.pop('gp')           # 取出並刪除
post.pop('views', None)       # 安全刪除，key 不存在也不會錯
post.clear()                  # 清空
```

### 3-4 常用操作

```python
post = {'title': '爆文', 'gp': 99, 'author': 'rc_dev'}

len(post)                # 3
'title' in post          # True（檢查 key 是否存在）
'爆文' in post.values()   # True（檢查 value）

post.keys()              # dict_keys(['title', 'gp', 'author'])
post.values()            # dict_values(['爆文', 99, 'rc_dev'])
post.items()             # dict_items([('title', '爆文'), ('gp', 99), ...])

# 合併兩個 dict
extra = {'board': 'Gossiping'}
post.update(extra)       # 把 extra 合併進 post

# Python 3.9+ 新語法
merged = post | extra    # 合併成新 dict
```

### 3-5 迴圈遍歷

```python
post = {'title': '爆文', 'gp': 99, 'author': 'rc_dev'}

# 只跑 key
for key in post:
    print(key)

# 同時拿 key 和 value（最常用）
for key, value in post.items():
    print(f'{key}: {value}')

# Dict comprehension
scores = {'A': 50, 'B': 99, 'C': 30}
viral = {k: v for k, v in scores.items() if v >= 99}
# 結果：{'B': 99}
```

---

## 四、爬蟲實戰：List 裝 Dict（超重要）

這是你專案最常遇到的結構——**一個 list，裡面裝很多 dict**，每個 dict 代表一篇文章。

```python
# 從論壇爬下來的爆文列表
viral_posts = [
    {'title': '爆文1', 'gp': 150, 'url': 'https://...', 'board': '電蝦'},
    {'title': '爆文2', 'gp': 99,  'url': 'https://...', 'board': 'Stock'},
    {'title': '爆文3', 'gp': 200, 'url': 'https://...', 'board': 'C_Chat'},
]

# 取第一篇的標題
print(viral_posts[0]['title'])   # '爆文1'

# 取所有標題
titles = [post['title'] for post in viral_posts]

# 篩選 GP 超過 100 的文章
super_viral = [p for p in viral_posts if p['gp'] > 100]

# 依 GP 由高到低排序
sorted_posts = sorted(viral_posts, key=lambda p: p['gp'], reverse=True)

# 遍歷處理
for post in viral_posts:
    print(f"[{post['board']}] {post['title']} - GP: {post['gp']}")
```

---

## 五、常見踩雷點 🚨

### 雷點 1：用 `[ ]` 取不存在的 key 會報錯

```python
post = {'title': '爆文'}

# ❌ 會噴 KeyError
# post['gp']

# ✅ 用 get() 安全取值
post.get('gp', 0)   # 沒有就回傳 0
```

### 雷點 2：Dict 不能用 list 當 key（不可變才能當 key）

```python
# ❌ TypeError: unhashable type: 'list'
# d = {[1, 2]: 'value'}

# ✅ 用 tuple 就可以
d = {(1, 2): 'value'}
```

### 雷點 3：把 dict 當成字串儲存會失去數值比較能力

你之前有碰過這個問題——記得嗎？

```python
# ❌ 這樣存，'99' 和 '120' 是字串，比較會亂掉
post = {'gp': '99'}   # '99' > '120' 會是 True（字串比較！）

# ✅ 存成數值
post = {'gp': 99}     # 99 > 120 才是正確的數值比較
```

### 雷點 4：list 的淺拷貝陷阱

```python
a = [1, 2, 3]
b = a              # ❌ 這不是複製，b 和 a 指向同一個 list
b.append(4)
print(a)           # [1, 2, 3, 4]（a 也被改了！）

# ✅ 真正複製
b = a.copy()       # 或 b = a[:] 或 b = list(a)
```

### 雷點 5：在迴圈中修改正在遍歷的 list

```python
posts = ['A', 'B', 'C', 'D']

# ❌ 邊跑邊刪，會跳過某些元素
for p in posts:
    if p == 'B':
        posts.remove(p)

# ✅ 跑副本，或用 list comprehension
posts = [p for p in posts if p != 'B']
```

---

## 六、速查表

### List 方法

| 方法 | 作用 | 範例 |
|------|------|------|
| `append(x)` | 尾端新增 | `lst.append(5)` |
| `insert(i, x)` | 插入到位置 i | `lst.insert(0, 'A')` |
| `extend(iter)` | 合併另一個 list | `lst.extend([1,2])` |
| `remove(x)` | 刪除值為 x 的第一個 | `lst.remove('A')` |
| `pop(i)` | 取出並刪除位置 i | `lst.pop(0)` |
| `index(x)` | 找 x 的位置 | `lst.index('A')` |
| `count(x)` | x 出現幾次 | `lst.count('A')` |
| `sort()` | 原地排序 | `lst.sort(reverse=True)` |
| `reverse()` | 原地反轉 | `lst.reverse()` |
| `copy()` | 淺拷貝 | `new = lst.copy()` |

### Dict 方法

| 方法 | 作用 | 範例 |
|------|------|------|
| `get(k, default)` | 安全取值 | `d.get('gp', 0)` |
| `keys()` | 所有 key | `d.keys()` |
| `values()` | 所有 value | `d.values()` |
| `items()` | 所有 (k, v) 對 | `d.items()` |
| `update(d2)` | 合併 | `d.update({'x':1})` |
| `pop(k)` | 取出並刪除 | `d.pop('gp')` |
| `setdefault(k, v)` | key 不存在時設預設值 | `d.setdefault('gp', 0)` |
| `clear()` | 清空 | `d.clear()` |

---

## 七、決策樹：我該用哪個？

```
要存的資料是什麼？
│
├─ 同類型、有順序的一堆東西
│  （文章清單、分數、使用者列表）
│  → 用 List [ ]
│
├─ 一筆資料有很多屬性
│  （一篇文章的 title/gp/author/url）
│  → 用 Dict { }
│
└─ 很多筆資料，每筆都有多種屬性
   （多篇文章，每篇都有 title/gp/author）
   → List 裝 Dict：[ {..}, {..}, {..} ]
   ← 你的爬蟲專案最常用！
```
