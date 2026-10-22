// Read-only extraction of the rendered listing. Run via Chrome DevTools evaluate_script.
() => {
  const main = document.querySelector('main');
  const articles = [...document.querySelectorAll('article')].filter(el => el.querySelector('h2 a, a h2'));
  const products = articles.map(article => {
    const heading = article.querySelector('h2');
    const link = heading?.closest('a') || heading?.querySelector('a');
    return {
      name: heading?.innerText,
      listingUrl: link?.href,
      directoryText: article.innerText,
      images: [...article.querySelectorAll('img')].map(img => ({ alt: img.alt, url: img.currentSrc || img.src })),
      screenshotLabels: [...article.querySelectorAll('button')].filter(b => /screenshot/i.test(b.getAttribute('aria-label') || b.innerText)).map(b => b.getAttribute('aria-label') || b.innerText),
    };
  });
  const pagination = [...document.querySelectorAll('a')].filter(a => a.href.includes('?p=')).map(a => ({ text: a.innerText, url: a.href }));
  const next = pagination.find(a => /Show more .* alternatives/.test(a.text))?.url || pagination.find(a => a.text.trim() === '❯')?.url || null;
  return { url: location.href, retrievedAt: new Date().toISOString(), title: document.title, heading: document.querySelector('h1')?.innerText, text: main?.innerText, products, pagination, next };
}
