using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.Rendering;
using TP2.Models;
using TP2.Models.Repositories;

namespace TP2.Controllers
{
    public class ProductController : Controller
    {
        private readonly IProductRepository ProductRepository;
        private readonly ICategorieRepository CategRepository;
        private readonly IWebHostEnvironment hostingEnvironment;

        public ProductController(IProductRepository ProdRepository, ICategorieRepository categRepository, IWebHostEnvironment hostingEnvironment)
        {
            ProductRepository = ProdRepository;
            CategRepository = categRepository;
            this.hostingEnvironment = hostingEnvironment;
        }

        // GET: Product
        public ActionResult Index(string term)
        {
            var products = ProductRepository.GetAll();

            if (!string.IsNullOrEmpty(term))
            {
                products = ProductRepository.FindByName(term);
            }

            // Spécifier explicitement la vue IndexProduct.cshtml
            return View("IndexProduct", products);
        }

        // GET: Product/Search (Page 12 du TP)
        public ActionResult Search(string val)
        {
            var result = ProductRepository.FindByName(val);
            return View("IndexProduct", result);
        }

        // GET: Product/Create
        public ActionResult Create()
        {
            ViewBag.CategoryId = new SelectList(CategRepository.GetAll(), "CategoryId", "CategoryName");
            // Spécifier explicitement la vue CreateProduct.cshtml
            return View("CreateProduct");
        }

        // POST: Product/Create
        [HttpPost]
        [ValidateAntiForgeryToken]
        public ActionResult Create(Product product, IFormFile? file)
        {
            if (ModelState.IsValid)
            {
                if (file != null)
                {
                    string uploadsFolder = Path.Combine(hostingEnvironment.WebRootPath, "images");
                    if (!Directory.Exists(uploadsFolder))
                    {
                        Directory.CreateDirectory(uploadsFolder);
                    }
                    string uniqueFileName = Guid.NewGuid().ToString() + "_" + file.FileName;
                    string filePath = Path.Combine(uploadsFolder, uniqueFileName);
                    using (var fileStream = new FileStream(filePath, FileMode.Create))
                    {
                        file.CopyTo(fileStream);
                    }
                    product.ImagePath = uniqueFileName;
                }

                ProductRepository.Add(product);
                return RedirectToAction(nameof(Index));
            }

            // En cas d'erreur de validation, recharger la liste des catégories et la vue CreateProduct.cshtml
            ViewBag.CategoryId = new SelectList(CategRepository.GetAll(), "CategoryId", "CategoryName", product.CategoryId);
            return View("CreateProduct", product);
        }
    }
}