"use strict";

(() => {
  const form = document.querySelector("#filters");
  const query = document.querySelector("#query");
  const year = document.querySelector("#year");
  const status = document.querySelector("#result-count");
  const normalize = (text) => text.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();
  const groups = [...document.querySelectorAll(".year-group")].map((section) => ({
    section,
    year: section.dataset.year,
    count: section.querySelector(".year-count"),
    navigation: document.querySelector(`.year-nav a[data-year="${section.dataset.year}"]`),
    entries: [...section.querySelectorAll(".entry")].map((entry) => ({
      entry,
      text: normalize([...entry.querySelectorAll("h3, .thesis, .supervisors")].map((el) => el.textContent).join(" ")),
    })),
  }));
  const total = groups.reduce((sum, group) => sum + group.entries.length, 0);

  function filter() {
    const terms = normalize(query.value).trim().split(/\s+/).filter(Boolean);
    let matches = 0;
    for (const group of groups) {
      let count = 0;
      for (const record of group.entries) {
        const visible = (!year.value || year.value === group.year) && terms.every((term) => record.text.includes(term));
        record.entry.hidden = !visible;
        if (visible) count++;
      }
      group.section.hidden = count === 0;
      group.navigation.hidden = count === 0;
      group.count.textContent = `(${count})`;
      matches += count;
    }
    status.textContent = matches === total ? `Showing all ${total} records` : `Showing ${matches} of ${total} records`;
    document.querySelector("#empty-state").hidden = matches !== 0;
    document.querySelector(".year-nav").hidden = matches === 0;
  }

  form.hidden = false;
  query.addEventListener("input", filter);
  year.addEventListener("change", filter);
  form.addEventListener("submit", (event) => event.preventDefault());
  form.addEventListener("reset", () => {
    query.value = "";
    year.value = "";
    filter();
  });
  window.addEventListener("pageshow", filter);
  filter();
})();
