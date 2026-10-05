using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;

namespace TP2.Models
{
    public class Category
    {
        public int CategoryId { get; set; }

        [Required(ErrorMessage = "Le nom de la catégorie est obligatoire")]
        [Display(Name = "Nom")]
        public string CategoryName { get; set; }

        // Ajouter '?' pour autoriser null lors de la validation du formulaire
        public ICollection<Product>? Products { get; set; }
    }
}