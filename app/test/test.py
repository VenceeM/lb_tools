

def test (**args):
    print(args)
    for key,value in args.items():
        print(f"{key}")
        
test(name="Test",lastname="Ok")