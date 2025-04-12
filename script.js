document.addEventListener("DOMContentLoaded", function () {
    const ordersContainer = document.getElementById("orders-container");
    const chatContainer = document.getElementById("chat-container");
    const chatInput = document.getElementById("chat-input");
    const sendMessageButton = document.getElementById("send-message");
    const toggleDarkModeButton = document.getElementById("toggle-dark-mode");

    async function fetchOrders() {
        const response = await fetch("/orders");
        const orders = await response.json();
        ordersContainer.innerHTML = "";
        orders.forEach(order => {
            const orderDiv = document.createElement("div");
            orderDiv.className = "order";
            orderDiv.innerHTML = `<p>رقم الطلب: ${order.id}</p>
                                  <p>الحالة: ${order.status}</p>
                                  <p>المطعم: ${order.restaurant}</p>
                                  <p>📍 الموقع: <a href="https://maps.google.com?q=${order.location}" target="_blank">رؤية على الخريطة</a></p>
                                  <button onclick="updateOrder(${order.id})">تم التوصيل</button>`;
            ordersContainer.appendChild(orderDiv);
        });
    }

    window.updateOrder = async function (id) {
        await fetch("/update_order", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ id, status: "تم التوصيل" }) });
        fetchOrders();
    };

    toggleDarkModeButton.addEventListener("click", () => {
        document.body.classList.toggle("dark-mode");
    });

    sendMessageButton.addEventListener("click", () => {
        const message = chatInput.value;
        if (message) {
            const messageDiv = document.createElement("div");
            messageDiv.innerText = `🗣️ ${message}`;
            chatContainer.appendChild(messageDiv);
            chatInput.value = "";
        }
    });

    fetchOrders();
});
