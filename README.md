# Darhan Bektaban Ailippe (AlphaBet)

![License](https://img.shields.io/badge/license-MIT-blue.svg) ![Version](https://img.shields.io/badge/version-1.1-green.svg) ![Language](https://img.shields.io/badge/language-Kazakh-blue)

**Darhan Bektaban Ailippe** is a standardized Latin-based alphabet system and "QAZ" keyboard layout for the Kazakh language.

This repository provides the official character mapping rules, machine-readable logic (`.json`), and conversion tools (`.py`) to facilitate the adoption of this script in digital systems and AI training.

## 🔤 The Alphabet Rules

The system uses a strictly logical mapping designed for the QWERTY keyboard. Mapping is derived directly from `ailippe_map.json` (Version 1.1).

| Cyrillic | Latin (DB Ailippe) | Note |
| :--- | :--- | :--- |
| **А а** | **A a** | |
| **Ә ә** | **Ai ai** | Digraph |
| **Б б** | **B b** | |
| **Д д** | **D d** | |
| **Е е / Э э** | **E e** | |
| **Г г** | **G g** | |
| **Ғ ғ** | **Gh gh** | Digraph |
| **Х х / Һ һ**| **H h** | Maps two Cyrillic chars to one Latin char |
| **І і** | **I i** | |
| **И и / Й й**| **J j** | Phonetic mapping |
| **К к** | **K k** | |
| **Л л** | **L l** | |
| **М м** | **M m** | |
| **Н н** | **N n** | |
| **Ң ң** | **Gn gn** | Digraph (Distinct from N) |
| **О о** | **O o** | |
| **Ө ө** | **Uoi uoi** | Trigraph |
| **П п** | **P p** | |
| **Қ қ** | **Q q** | Key component of "QAZ" layout |
| **Р р** | **R r** | |
| **С с** | **S s** | |
| **Ш ш** | **Sh sh** | Digraph |
| **Т т** | **T t** | |
| **Ұ ұ** | **U u** | |
| **Ү ү** | **Ui ui** | Digraph |
| **У у** | **Uu uu** | Double U |
| **Ы ы** | **Y y** | |
| **З з** | **Z z** | |
| **Ж ж** | **Zh zh** | Digraph |
| **Ю ю** | **Juu juu** | Standard Mapping |
| **Я я** | **Ja ja** | Standard Mapping |
| **В в** | **V v** | Loan letter |
| **Ф ф** | **F f** | Loan letter |
| **Ц ц** | **Ts ts** | Loan letter |
| **Ч ч** | **Ch ch** | Loan letter |
| **Щ щ** | **Shch shch** | Loan letter |
| **Ё ё** | **Jo jo** | Loan letter |
| **Ь ь** | **'** | Soft Sign (Apostrophe) |
| **Ъ ъ** | **J j** | Loan letter |

### Special Context Rules
These rules (defined in `logic.forward.special_rules`) have **Priority 1**. They override the standard single-letter mapping to preserve accurate pronunciation.

| Sequence | Maps to | Example Input | Example Output |
| :--- | :--- | :--- | :--- |
| **ция** | **sja** | Авиа**ция** | Avja**sja** |
| **цио** | **sjo** | Ак**цио**нер | Ak**sjo**ner |
| **ия** | **ja** | Аз**ия** | Az**ja** |

---

## 💻 Technical Usage

This repository includes a Python script (`translator.py`) that uses the rules defined in `ailippe_map.json`.

### 1. Installation
Clone the repository:
```bash
git clone [https://github.com/DarhanBektaban/Ailippe.git](https://github.com/DarhanBektaban/Ailippe.git)
cd Ailippe
