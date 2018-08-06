// List of residual equations for the coupled Allen-Cahn example application

// =================================================================================
// Set the attributes of the primary field variables
// =================================================================================
void variableAttributeLoader::loadVariableAttributes(){
	// Variable 0
	set_variable_name				(0,"n");
	set_variable_type				(0,SCALAR);
	set_variable_equation_type		(0,PARABOLIC);

	set_need_value					(0,true);
	set_need_gradient				(0,true);
	set_need_hessian				(0,false);

	set_need_value_residual_term	(0,true);
	set_need_gradient_residual_term	(0,true);

    set_variable_name				(1,"psi");
	set_variable_type				(1,VECTOR);
	set_variable_equation_type		(1,ELLIPTIC);
}

Test to see /* how block comments */ are /* treated */

one /* more block
comments test
this time */ for multiline cases

finally /*
testing */ multiple /*
kinds */ of /* block */ comments
