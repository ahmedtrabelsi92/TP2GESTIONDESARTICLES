using Microsoft.AspNetCore.Mvc;
using TP2.Models;
using TP2.Models.Repositories;

namespace TP2.Controllers
{
    public class CategoryController : Controller
    {
        private readonly ICategorieRepository CategRepository;

        public CategoryController(ICategorieRepository categRepository)
        {
            CategRepository = categRepository;
        }

        // GET: Category
        public ActionResult Index()
        {
            var categories = CategRepository.GetAll();
            // Spécifier explicitement le nom de la vue "IndexCategory"
            return View("IndexCategory", categories);
        }

        // GET: Category/Create
        public ActionResult Create()
        {
            // Spécifier explicitement le nom de la vue "CreateCategory"
            return View("CreateCategory");
        }

        // POST: Category/Create
        [HttpPost]
        [ValidateAntiForgeryToken]
        public ActionResult Create([Bind("CategoryId,CategoryName")] Category category)
        {
            if (ModelState.IsValid)
            {
                CategRepository.Add(category);
                return RedirectToAction(nameof(Index));
            }
            // En cas d'erreur de validation, recharger CreateCategory.cshtml
            return View("CreateCategory", category);
        }

        // GET: Category/Edit/5
        public ActionResult Edit(int id)
        {
            var category = CategRepository.GetById(id);
            if (category == null)
            {
                return NotFound();
            }
            return View(category);
        }

        // POST: Category/Edit/5
        [HttpPost]
        [ValidateAntiForgeryToken]
        public ActionResult Edit(Category category)
        {
            if (ModelState.IsValid)
            {
                CategRepository.Update(category);
                return RedirectToAction(nameof(Index));
            }
            return View(category);
        }

        // GET: Category/Delete/5
        public ActionResult Delete(int id)
        {
            var category = CategRepository.GetById(id);
            if (category == null)
            {
                return NotFound();
            }
            return View(category);
        }

        // POST: Category/Delete/5
        [HttpPost, ActionName("Delete")]
        [ValidateAntiForgeryToken]
        public ActionResult DeleteConfirmed(int id)
        {
            CategRepository.Delete(id);
            return RedirectToAction(nameof(Index));
        }
    }
}