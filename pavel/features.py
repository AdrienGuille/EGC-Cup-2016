from clustering.models import build_unsup_base_model

__author__ = 'Pavel Soriano'
__mail__ = 'sorianopavel@gmail.com'



def apply_models():
    mod1 = build_unsup_base_model()

    models =[mod1]
def main():
    apply_models()
    # my code here

if __name__ == "__main__":
    main()