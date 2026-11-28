const QUEST_TASKS = [
    "Знайди загублений ключ у старій вежі до заходу сонця.",
    "Проведи караван через туманний ліс, оминаючи пастки.",
    "Розшифруй руни на дверях підземного храму.",
    "Врятуй мандрівника з пазурів болотного дракона.",
    "Доберися до маяка і запали вогонь, поки шторм не накрив берег."
];

const INVENTORY_POOL = [
    "Сталевий меч",
    "Щит вартового",
    "Зілля зцілення",
    "Ліхтар мандрівника",
    "Мотузка",
    "Карта підземель"
];

const questText = document.getElementById("quest-text");
const questButton = document.getElementById("quest-button");
const inventoryList = document.getElementById("inventory-list");
const inventoryButton = document.getElementById("inventory-button");

questButton.addEventListener("click", () => {
    const index = Math.floor(Math.random() * QUEST_TASKS.length);
    questText.textContent = QUEST_TASKS[index];
});

inventoryButton.addEventListener("click", () => {
    const pool = INVENTORY_POOL.slice();
    const selected = [];

    while (selected.length < 3) {
        const index = Math.floor(Math.random() * pool.length);
        selected.push(pool.splice(index, 1)[0]);
    }

    inventoryList.replaceChildren();

    selected.forEach((item) => {
        const listItem = document.createElement("li");
        listItem.textContent = item;
        inventoryList.appendChild(listItem);
    });
});
