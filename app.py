
import streamlit as st
import fitz  # PyMuPDF
import io

st.set_page_config(page_title="توقيع PDF", layout="centered")
st.title("📄 إضافة توقيع إلى ملف PDF")

pdf_file = st.file_uploader("📤 اختر ملف PDF", type="pdf")
image_file = st.file_uploader("🖋️ اختر صورة التوقيع", type=["png", "jpg", "jpeg"])

if pdf_file and image_file:
    if st.button("✍️ تنفيذ التوقيع"):
        try:
            pdf_bytes = pdf_file.read()
            img_bytes = image_file.read()

            doc = fitz.open("pdf", pdf_bytes)
            for page in doc:
                rect = page.rect
                x0 = rect.x0 + 50
                y0 = rect.y1 - 120
                x1 = x0 + 300
                y1 = y0 + 100
                image_rect = fitz.Rect(x0, y0, x1, y1)
                page.insert_image(image_rect, stream=img_bytes)

            output = io.BytesIO()
            doc.save(output)
            doc.close()

            st.success("✅ تم توقيع الملف بنجاح!")
            st.download_button("📥 تحميل الملف الموقع", data=output.getvalue(), file_name="signed_output.pdf", mime="application/pdf")

        except Exception as e:
            st.error(f"حدث خطأ: {e}")
