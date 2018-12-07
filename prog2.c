int main() {
	
	/*Arquivo executa como deveria, todavia está programado um loop infinito que vai printar
	0 1 2 3 4 5 6 6 6 6 .....*/

	int x, i;
	
	i = 0;
	while(i < 10) {
		if(i > 5) {
			print(i);
			continue;
		}
		i = i + 1;
		print(i, "\n");
	}

	print(x, "\n");

	return 0;
}