from flask import Flask, render_template, request, redirect, url_for, send_file
from db import db, init_db
import pandas as pd

# Khởi tạo Flask app
app = Flask(__name__)

# Kết nối cơ sở dữ liệu
init_db(app)

# Mô hình dữ liệu cho bảng Vehicle
class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    license_plate = db.Column(db.String(20), nullable=False)
    code = db.Column(db.String(20), nullable=False)
    time = db.Column(db.String(50), nullable=False)

# Tạo bảng trong cơ sở dữ liệu nếu chưa có
with app.app_context():
    db.create_all()

# Trang chủ
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        license_plate = request.form.get("license_plate")
        code = request.form.get("code")
        time = request.form.get("time")

        # Lưu thông tin vào cơ sở dữ liệu
        new_vehicle = Vehicle(license_plate=license_plate, code=code, time=time)
        db.session.add(new_vehicle)
        db.session.commit()

    vehicles = Vehicle.query.all()
    return render_template("index.html", vehicles=vehicles)

# Xóa thông tin xe
@app.route("/delete/<int:id>")
def delete(id):
    vehicle = Vehicle.query.get(id)
    if vehicle:
        db.session.delete(vehicle)
        db.session.commit()
    return redirect(url_for("index"))

# Xuất thông tin xe thành file Excel
@app.route("/export")
def export():
    vehicles = Vehicle.query.all()
    data = [{"Biển số xe": v.license_plate, "Mã số gửi xe": v.code, "Thời gian lấy xe": v.time} for v in vehicles]
    df = pd.DataFrame(data)

    file_path = "vehicle_info.xlsx"
    df.to_excel(file_path, index=False)

    return send_file(file_path, as_attachment=True)

# Chạy ứng dụng
if __name__ == "__main__":
    app.run(debug=True)
