function openModal(title, phone, price, desc, img) {
document.getElementById("modalTitle").innerText = title;
document.getElementById("modalPhone").innerText = "Contact: " + phone;
document.getElementById("modalPrice").innerText = price;
document.getElementById("modalDesc").innerText = desc;
document.getElementById("modalImg").src = img;
}

function bookingSuccess(){
alert("Booking Successful! Our team will contact you soon.");
$('#bookingModal').modal('hide');
}