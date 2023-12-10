Hệ thống lọc cộng tác (CF) và đề xuất dựa trên máy tính thường liên quan đến nguồn gốc của hệ thống có tên Tapestry.

Một trong những thuộc tính chính của hệ thống này là nó cho phép tạo ra các đề xuất dựa trên sự kết hợp các ý tưởng đầu vào từ nhiều người dùng khác. Thay vì lọc các mục dựa trên nội dung, việc đưa ra đề xuất dựa trên ý kiến của những người dùng có cùng quan điểm đã trở nên phổ biến được gọi là lọc cộng tác. 

Về cơ bản thì hệ thống này nó có hai loại: 
  
  + Lọc dựa trên người dùng (User – User): Các hệ thống này giới thiệu sản phẩm cho người dùng mà những người dùng tương tự đã thích. Để đo lường sự giống nhau giữa hai người dùng, chúng ta có thể sử dụng tương quan Pearson hoặc độ tương tự cosine. Kỹ thuật lọc này có thể được minh họa bằng một ví dụ.
    
    ![image](https://github.com/manaxmaaxn/ML231/assets/127325509/a7ec42b0-ca42-49a8-8b85-a7abeebe0102)

    Vì người dùng A và F không chia sẻ bất kỳ xếp hạng phim nào chung với người dùng E nên điểm tương đồng của họ với người dùng E không được xác định trong Pearson Correlation. Do đó, chúng ta chỉ cần xét người dùng B, C và D. Dựa trên Tương quan Cosine Similatiry, chúng ta có thể tính toán độ tương tự sau.
    Similarity = cos(θ)=(A .B)/(|A||B|  )=  (∑_(i=1)^n▒〖A_i B_i 〗)/(√(∑_(i=1)^n▒〖A_i〗^2 ) √(∑_(i=1)^n▒〖B_i〗^2 ))
 


    
