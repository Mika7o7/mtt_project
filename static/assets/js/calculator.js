document.addEventListener("DOMContentLoaded", () => {
  let map, route;
  const fromInput = document.getElementById("from");
  const toInput = document.getElementById("to");
  const distanceField = document.querySelector(".clt_km--js");
  const priceField = document.querySelector(".clt_sum--js");
  const phoneInput = document.querySelector("input[name='f_phone']");

  // Маска телефона
  if (phoneInput) {
    IMask(phoneInput, { mask: "+{7}(000)000-00-00" });
  }

  ymaps.ready(() => {
    map = new ymaps.Map("map_map", {
      center: [55.751574, 37.573856],
      zoom: 9,
      controls: ["zoomControl"],
    });

    // Подключаем подсказки адресов
    const suggestViewFrom = new ymaps.SuggestView("from");
    const suggestViewTo = new ymaps.SuggestView("to");

    document.getElementById("build-route").addEventListener("click", async () => {
      const from = fromInput.value.trim();
      const to = toInput.value.trim();

      if (!from || !to) {
        alert("Пожалуйста, введите оба адреса.");
        return;
      }

      // Удаляем старый маршрут
      if (route) map.geoObjects.remove(route);

      try {
        const newRoute = await ymaps.route([from, to]);
        route = newRoute;
        map.geoObjects.add(route);
        map.setBounds(route.getBounds(), { checkZoomRange: true });

        // Получаем длину маршрута в км
        const distance = Math.round(route.getLength() / 1000);
        distanceField.value = distance;

        // Простая формула: 100 + 20 * км
        const price = 100 + distance * 20;
        priceField.textContent = price.toLocaleString("ru-RU");

      } catch (err) {
        console.error(err);
        alert("Не удалось построить маршрут. Проверьте адреса.");
      }
    });
  });
});
