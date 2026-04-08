import os
from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display

class QudratGenerator:
    def __init__(self, font_path):
        self.font_path = font_path
        # الألوان الأساسية للتصميم
        self.colors = {
            "bg": (255, 255, 255),          # أبيض للخلفية
            "sidebar": (205, 126, 110),     # اللون الجانبي
            "box": (245, 245, 245),         # خلفية السؤال الرمادية
            "footer": (255, 82, 82),        # شريط الإجابة الأحمر
            "text_q": (50, 50, 100),        # لون نص السؤال
            "text_opt": (0, 0, 0),          # لون نص الخيارات
            "white": (255, 255, 255)        # لون نص الإجابة
        }

    def _format_ar(self, text):
        """تجهيز وتحويل النص العربي ليعرض بشكل صحيح"""
        reshaped = arabic_reshaper.reshape(text)
        return get_display(reshaped)

    def generate_image(self, question, options, correct_ans, output_name="result.png"):
        # أبعاد الصورة
        width, height = 1200, 630
        img = Image.new('RGB', (width, height), color=self.colors["bg"])
        draw = ImageDraw.Draw(img)

        # تحميل الخط (تأكد من وجود الملف في مجلد المشروع)
        try:
            font_q = ImageFont.truetype(self.font_path, 35)
            font_opt = ImageFont.truetype(self.font_path, 30)
            font_res = ImageFont.truetype(self.font_path, 45)
        except OSError:
            print(f"خطأ: لم يتم العثور على الخط في {self.font_path}")
            return

        # 1. رسم العناصر الهيكلية
        # الشريط الجانبي الأيمن
        draw.rounded_rectangle([1020, 150, 1150, 520], radius=25, fill=self.colors["sidebar"])
        # مربع السؤال
        draw.rounded_rectangle([100, 150, 1000, 480], radius=20, fill=self.colors["box"])
        # شريط الإجابة بالأسفل
        draw.rounded_rectangle([100, 480, 1000, 530], radius=5, fill=self.colors["footer"])

        # 2. كتابة النصوص
        # كتابة السؤال
        draw.text((970, 190), self._format_ar(question), fill=self.colors["text_q"], font=font_q, anchor="rm")

        # كتابة الخيارات
        labels = ['أ', 'ب', 'ج', 'د']
        coords = [(750, 300), (350, 300), (750, 380), (350, 380)]
        for i, (opt, pos) in enumerate(zip(options, coords)):
            full_txt = f"{labels[i]}) {opt}"
            draw.text(pos, self._format_ar(full_txt), fill=self.colors["text_opt"], font=font_opt, anchor="rm")

        # كتابة الإجابة الصحيحة
        ans_txt = f"الإجابة: {correct_ans}"
        draw.text((550, 505), self._format_ar(ans_txt), fill=self.colors["white"], font=font_res, anchor="mm")

        # 3. حفظ الصورة
        img.save(output_name)
        print(f"✅ تم حفظ الصورة بنجاح باسم: {output_name}")

# --- تجربة الكود ---
if __name__ == "__main__":
    # ملاحظة: حمل خط Tajawal-Bold.ttf وضعه بجانب الكود
    generator = QudratGenerator("Tajawal-Bold.ttf")

    my_data = {
        "question": "عند مخالطة شخص مصاب بالإنفلونزا لمجموعة غير مصابة وفقاً للفقرة (5) فإن ذلك يؤدي إلى ....",
        "options": ["حضانة الفيروس", "انتقال الفيروس", "إضعاف الفيروس", "اكتشاف الفيروس"],
        "correct": "ب"
    }

    generator.generate_image(my_data["question"], my_data["options"], my_data["correct"])
