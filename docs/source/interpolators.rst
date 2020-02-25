Interpolators
=============

An "interpolator" is a class which knows how to get values from a particular
source by interpreting the internal portion of a dynamic config value
and replacing it with a value.

Default included interpolators include:

* ENV (environment variables)
* FILE (file data)

You can use all registered interpolators when loading the configuration

.. code-block:: yml

   namespace:
     env: <% ENV[ENV, production] %>
     log_level: DEBUG
     ssl_cert: FILE[ssl_cert.crt]

     theoretical_http_loaded_value: <% HTTP[localhost:5000/variable, 3] %>

The point is that all pieces of individual configuration can be defined
centrally and declaratively, while interpolators actually go obtain that
config value associate with the given input.

Configly allows the dynamic addition of new interpolator through the use of
the :func:`register_interpolator` function.
