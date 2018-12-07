int main() {
	
	
	/*Aparentemente o esquema de blocos está tudo OK, ao menos tudo que consegui testar.*/

	int a,b,c,d;
	
	a = 1 + 2; 
	b = 3 - 1; 
	c = a * b; 
	d = 2; 

	/*Para dar certo*/
	if(1==1){
		int e;
		int a;
		a = 8;
		e=1;
		print(a,"\n");

		if(2==2){
			a = 1;
			print(e,"\n");

		}

	}

	if(1==1){
		int a;
		a=10;
		print(a,"\n");
		print(c,"\n");
	}

	/*Para dar errado
	if(1==1){
		int e;
		e=1;
		print(e);
	}
	print(e)
	*/

	print("a= ",a,"\n");
	print("b= ",b,"\n");
	print("c= ",c,"\n");
	print("d= ",d,"\n");

    return 0;
}