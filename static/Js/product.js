const API_BASE = "/store/api/"; // eğer urls farklıysa düzelt
// But bizim urls tanımı: /store/api/... değilse direkt "/api/product/"

const pdUrl = `/api/products/${productId}/`;
const reviewsUrl = `/api/products/${productId}/reviews/`;
const postReviewUrl = `/api/products/${productId}/reviews/create/`;

function renderStars(avg) {
  let html = "";
  const full = Math.floor(avg);
  for (let i=1;i<=5;i++){
    if (i<=full) html += '<i class="bi bi-star-fill text-warning"></i>';
    else html += '<i class="bi bi-star text-muted"></i>';
  }
  html += `<span class="ms-2 text-muted">(${avg})</span>`;
  return html;
}

function loadProduct() {
  fetch(pdUrl)
    .then(r=>r.json())
    .then(p=>{
      document.getElementById("product-name").innerText = p.name;
      document.getElementById("product-price").innerText = p.price + " TL";
      document.getElementById("main-image").src = p.image_url || (p.images && p.images[0]) || "/static/images/no-image.png";

      // badges
      if (p.is_premium) document.getElementById("badge-premium").style.display = "inline-block";
      if (p.has_video) document.getElementById("badge-video").style.display = "inline-block";

      // thumbs
      const thumbs = document.getElementById("thumbs");
      thumbs.innerHTML = "";
      const imgs = p.images && p.images.length ? p.images : [p.image_url];
      imgs.forEach((url, idx) => {
        const img = document.createElement("img");
        img.src = url;
        img.className = "thumb-img";
        img.addEventListener("click", ()=> document.getElementById("main-image").src = url);
        thumbs.appendChild(img);
      });

      // rating
      document.getElementById("rating-area").innerHTML = renderStars(p.avg_rating) + `<span class="ms-2 text-muted">(${p.review_count} değerlendirme)</span>`;
      document.getElementById("review-count").innerText = p.review_count;

      // delivery days (örnek basit)
      const days = ["Bugün","Yarın","Yarın+1"];
      const dd = document.getElementById("delivery-days");
      dd.innerHTML = "";
      days.forEach((d,i)=>{
        const btn = document.createElement("button");
        btn.className = i===0 ? "btn btn-success" : "btn btn-outline-secondary";
        btn.innerText = d;
        btn.addEventListener("click", ()=> {
          // seçili stil
          document.querySelectorAll("#delivery-days button").forEach(b=>b.classList.remove("btn-success"));
          btn.classList.add("btn-success");
          loadHoursForDay(i);
        });
        dd.appendChild(btn);
      });

      loadHoursForDay(0);
    });
}

function loadHoursForDay(dayIndex) {
  const sel = document.getElementById("delivery-hours");
  sel.innerHTML = "";
  const hours = ["09:00 - 12:00","12:00 - 15:00","15:00 - 18:00"];
  hours.forEach(h=>{
    const opt = document.createElement("option");
    opt.value = h;
    opt.innerText = h;
    sel.appendChild(opt);
  });
}

function loadReviews() {
  fetch(reviewsUrl)
    .then(r=>r.json())
    .then(list=>{
      const container = document.getElementById("review-list");
      container.innerHTML = "";
      if (!list.length) {
        container.innerHTML = "<div class='text-muted'>Henüz yorum yok.</div>";
        return;
      }
      list.forEach(r=>{
        const el = document.createElement("div");
        el.className = "border rounded p-3 mb-2";
        el.innerHTML = `<strong>${r.name}</strong> • ⭐ ${r.rating}/5 <small class="text-muted ms-2">${new Date(r.created_at).toLocaleString()}</small>
                        <p class="mt-2">${r.comment}</p>`;
        container.appendChild(el);
      });
    });
}

// review form
document.addEventListener("DOMContentLoaded", ()=>{
  loadProduct();
  loadReviews();

  document.getElementById("review-form").addEventListener("submit", function(e){
    e.preventDefault();
    const name = document.getElementById("rev-name").value || "Misafir";
    const rating = document.getElementById("rev-rating").value;
    const comment = document.getElementById("rev-comment").value;
    fetch(postReviewUrl, {
      method: "POST",
      headers: {"Content-Type":"application/json", "X-CSRFToken": getCookie('csrftoken')},
      body: JSON.stringify({name, rating, comment})
    }).then(r=>{
      if (!r.ok) throw new Error("Hata");
      // temizle ve yenile
      document.getElementById("rev-name").value = "";
      document.getElementById("rev-rating").value = "5";
      document.getElementById("rev-comment").value = "";
      loadProduct(); // güncel ortalama + sayıyı çek
      loadReviews();
    }).catch(err=>{
      alert("Yorum kaydedilemedi");
    });
  });

  // sipariş butonu örnek: sepete ekle (session)
  document.getElementById("buy-btn").addEventListener("click", ()=>{
    fetch(`/api/cart/add/`, {
      method: "POST",
      headers: {"Content-Type":"application/json", "X-CSRFToken": getCookie('csrftoken')},
      body: JSON.stringify({product_id: productId, qty: 1})
    }).then(r=>r.json()).then(data=>{
      window.location.href = "/checkout/"; // veya sepete git
    });
  }); 

});

// yardımcı: csrf cookie al
function getCookie(name) {
  let v = document.cookie.match('(^|;) ?' + name + '=([^;]*)(;|$)');
  return v ? v[2] : null;
}

