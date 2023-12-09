# Lọc nhân khẩu học (Demographic Filtering)
Sẽ đưa ra các đề xuất tổng quát cho mọi người dùng, dựa trên mức độ phổ biến của phim và thể loại. Nói rõ hơn thì phương pháp này sẽ đề xuất những bộ phim giống nhau cho những người dùng có cùng đặc điểm nhân khẩu học. Demographic Filtering ban đầu sẽ dựa tập data có sẵn, và từ những người có cùng sở thích hoặc có cùng những hành vi xem phim giống nhau sẽ tạo ra các danh mục những người có cùng kiểu nhân khẩu học
    ![image](https://github.com/manaxmaaxn/ML231/assets/127325509/69bba1bc-6f73-4085-a0e4-70e509201f7f)

Tập dữ liệu mà nhóm sử dụng không có dữ liệu đầu vào cụ thể để phân chia theo các nhóm nhân khẩu học nên nhóm sẽ hướng đến sử dụng theo kiểu đề xuất dựa trên mức độ phổ biến của phim trên thể loại và nhóm cần một phương tiện để tính toán nên nhóm sẽ dùng hàm tính toán WR của IMDB:

Weighted Rating (WR)=(v/(v+m).R)+(m/(v+m).C)

Trong đó:

v: là tổng số vote của bộ phim đó

m: là lượng vote tối thiểu để có thể được liệt kê trong danh sách
R: là điểm số trung bình điểm đánh giá của bộ phim đó
C: là số lượng vote trung bình của toàn bộ tập dữ liệu
