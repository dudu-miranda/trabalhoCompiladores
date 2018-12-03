int main() {
	
	int n;
	int teste;
	n = 9 * 5 + (-3.5);
	print(n);

	if(n == 5) {
		print("Hmm");
	} else {
		print("Dois");
	}

    scan("Teste = ", teste);
    print(teste);

	int i;
	i = 0;
	while(i < teste) {
		print("Print", i);
		i = i + 1;
	}

	for(i = 0; i < 10; i = i + 1) {
		if(i > 5){
			teste = 0;
		}
		else{
			i++;
		}
	}
    
    n = teste * (6 + (-3)) / 9;
    print(n);
    print(teste);

    return 0;
}